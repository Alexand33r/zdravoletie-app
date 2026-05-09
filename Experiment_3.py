"""
Experiment 3 -- Feature Group Ablation
========================================
Four cumulative feature groups evaluated using the best model from Experiment 1
(HistGradientBoosting). Groups are additive:

  Group 1: Anthropometric & Metabolic         (~63 features)
  Group 2: + Bioimpedance                     (~73 features)
  Group 3: + Postural Risk                    (~83 features)
  Group 4: + Joint Angles  (all features)     (88 features)

30 repeated GroupShuffleSplits grouped by individual name. Reports MAE, RMSE,
and R2 as mean +/- 95% CI. Paired Wilcoxon signed-rank tests with Bonferroni
correction (6 group pairs = C(4,2)) determine statistical significance.

Known issue: aggregated_postural_index is included in the postural risk group
and is the arithmetic mean of 6 features also in that group. It adds no
independent information when all 6 components are present. Retained for
consistency with the trained model artifact; noted as Limitation 3 in
thesis/methodology.md.

Outputs written to results/:
  experiment_3_scores.csv         per-fold MAE / RMSE / R2 for all feature groups
  experiment_3_summary.csv        mean, std, 95% CI bounds per group x metric
  experiment_3_significance.csv   Wilcoxon statistics and Bonferroni-adjusted p-values
  experiment_3_boxplot.png        MAE / RMSE / R2 box plots across feature groups
  experiment_3_learning_curve.png mean MAE +/- 95% CI as feature count increases

Usage:
  python Experiment_3.py
"""

import json
import warnings
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler

import config

warnings.filterwarnings("ignore")
np.random.seed(config.RANDOM_SEED)

Path(config.DIR_RESULTS).mkdir(exist_ok=True)

# ── Best model from Experiment 1 ──────────────────────────────────────────────
BEST_MODEL_NAME = "HistGradientBoosting"

# ── Feature group definitions ─────────────────────────────────────────────────
# Groups are cumulative (each adds to the previous).
# Base group = model_features minus the three named additive groups.
with open(config.PATH_MODEL_FEATURES) as f:
    model_features = json.load(f)

BIOIMPEDANCE   = set(config.FEATURES_BIOIMPEDANCE)
POSTURAL_RISK  = set(config.FEATURES_POSTURAL_RISK)
JOINT_ANGLES   = set(config.FEATURES_JOINT_ANGLES)
ANTHRO_METABOLIC = set(model_features) - BIOIMPEDANCE - POSTURAL_RISK - JOINT_ANGLES

# Build ordered feature lists for each cumulative group
GROUP_1_FEATURES = sorted(ANTHRO_METABOLIC)
GROUP_2_FEATURES = sorted(ANTHRO_METABOLIC | BIOIMPEDANCE)
GROUP_3_FEATURES = sorted(ANTHRO_METABOLIC | BIOIMPEDANCE | POSTURAL_RISK)
GROUP_4_FEATURES = model_features  # all 88

FEATURE_GROUPS = {
    "G1_AnthroMetabolic":         GROUP_1_FEATURES,
    "G2_+Bioimpedance":           GROUP_2_FEATURES,
    "G3_+PosturalRisk":           GROUP_3_FEATURES,
    "G4_+JointAngles":            GROUP_4_FEATURES,
}
GROUP_NAMES = list(FEATURE_GROUPS.keys())
N_GROUP_PAIRS = len(list(combinations(GROUP_NAMES, 2)))  # C(4,2) = 6
BONFERRONI_ALPHA_E3 = config.ALPHA / N_GROUP_PAIRS  # 0.05 / 6 ≈ 0.0083

# ── Data loading ──────────────────────────────────────────────────────────────
print("Loading data...")
df = pd.read_csv(config.PATH_MASTER_CSV)

df["sex_encoded"] = df["sex"].map({"F": 0, "M": 1})
df["muscle_fat_ratio"] = df["muscle"] / (df["fat"] + 0.1)
df["upper_lower_muscle_ratio"] = df["upperBody"] / (df["lowerBody"] + 0.1)
limb_fat_cols = ["fatLeftArm", "fatRightArm", "fatLeftLeg", "fatRightLeg"]
df["trunk_limb_fat_ratio"] = df["fatTrunk"] / (df[limb_fat_cols].sum(axis=1) + 0.1)
postural_cols = ["humpbackRisk", "spineRisk", "pelvisRisk",
                 "postureRisk", "kneeRisk", "frontHeadRisk"]
df["aggregated_postural_index"] = df[postural_cols].mean(axis=1)
df.replace([np.inf, -np.inf], np.nan, inplace=True)

X_full = df[model_features].copy()
y_full = df["age_gap"].copy()
groups = df[config.GROUP_COLUMN]

print(f"  Dataset: {len(df)} records, {df[config.GROUP_COLUMN].nunique()} individuals")
print(f"\nFeature group sizes:")
for gname, gfeats in FEATURE_GROUPS.items():
    print(f"  {gname}: {len(gfeats)} features")


# ── Cross-validation loop ─────────────────────────────────────────────────────
print(f"\nRunning {config.N_CV_SPLITS} GroupShuffleSplits x {len(GROUP_NAMES)} feature groups...")

gss = GroupShuffleSplit(
    n_splits=config.N_CV_SPLITS,
    test_size=config.TEST_SIZE,
    random_state=config.RANDOM_SEED,
)

records = []

for split_index, (train_idx, test_idx) in enumerate(gss.split(X_full, y_full, groups=groups)):
    X_train_full = X_full.iloc[train_idx].copy()
    X_test_full  = X_full.iloc[test_idx].copy()
    y_train      = y_full.iloc[train_idx]
    y_test       = y_full.iloc[test_idx]

    # Impute with training-fold medians (computed on full feature set)
    fold_medians = X_train_full.median()
    X_train_full = X_train_full.fillna(fold_medians).fillna(0)
    X_test_full  = X_test_full.fillna(fold_medians).fillna(0)

    for group_name, group_feats in FEATURE_GROUPS.items():
        X_tr = X_train_full[group_feats].values
        X_te = X_test_full[group_feats].values

        scaler = StandardScaler()
        X_tr_sc = scaler.fit_transform(X_tr)
        X_te_sc = scaler.transform(X_te)

        hp = config.MODEL_HYPERPARAMS[BEST_MODEL_NAME]
        model = HistGradientBoostingRegressor(**hp)
        model.fit(X_tr_sc, y_train)
        y_pred = model.predict(X_te_sc)

        records.append({
            "split":        split_index,
            "group":        group_name,
            "n_features":   len(group_feats),
            "mae":          mean_absolute_error(y_test, y_pred),
            "rmse":         np.sqrt(mean_squared_error(y_test, y_pred)),
            "r2":           r2_score(y_test, y_pred),
            "n_test":       len(y_test),
        })

    if (split_index + 1) % 5 == 0:
        print(f"  Split {split_index + 1:2d} / {config.N_CV_SPLITS} done")

df_scores = pd.DataFrame(records)
df_scores.to_csv(f"{config.DIR_RESULTS}/experiment_3_scores.csv", index=False)
print(f"\nPer-fold scores saved ({len(df_scores)} rows).")


# ── Summary statistics with 95% CI ───────────────────────────────────────────
t_crit = stats.t.ppf((1 + config.CONFIDENCE_LEVEL) / 2, df=config.N_CV_SPLITS - 1)

summary_rows = []
for group_name in GROUP_NAMES:
    subset = df_scores[df_scores["group"] == group_name]
    n_feats = subset["n_features"].iloc[0]
    for metric in ["mae", "rmse", "r2"]:
        values  = subset[metric].values
        mean_v  = values.mean()
        std_v   = values.std(ddof=1)
        ci_half = t_crit * std_v / np.sqrt(config.N_CV_SPLITS)
        summary_rows.append({
            "group":      group_name,
            "n_features": n_feats,
            "metric":     metric.upper(),
            "mean":       round(mean_v,  4),
            "std":        round(std_v,   4),
            "ci_lower":   round(mean_v - ci_half, 4),
            "ci_upper":   round(mean_v + ci_half, 4),
        })

df_summary = pd.DataFrame(summary_rows)
df_summary.to_csv(f"{config.DIR_RESULTS}/experiment_3_summary.csv", index=False)

print("\nSummary (MAE by feature group):")
print(df_summary[df_summary["metric"] == "MAE"]
      [["group", "n_features", "mean", "std", "ci_lower", "ci_upper"]]
      .to_string(index=False))


# ── Wilcoxon tests with Bonferroni correction ─────────────────────────────────
sig_rows = []
group_pairs = list(combinations(GROUP_NAMES, 2))

for metric in ["mae", "rmse", "r2"]:
    pivot = df_scores.pivot(index="split", columns="group", values=metric)
    for group_a, group_b in group_pairs:
        statistic, p_raw = stats.wilcoxon(
            pivot[group_a].values,
            pivot[group_b].values,
            alternative="two-sided",
        )
        p_adjusted = min(p_raw * N_GROUP_PAIRS, 1.0)
        sig_rows.append({
            "metric":        metric.upper(),
            "group_a":       group_a,
            "group_b":       group_b,
            "wilcoxon_stat": round(statistic, 3),
            "p_raw":         round(p_raw,      6),
            "p_adjusted":    round(p_adjusted,  6),
            "significant":   p_adjusted < BONFERRONI_ALPHA_E3,
        })

df_sig = pd.DataFrame(sig_rows)
df_sig.to_csv(f"{config.DIR_RESULTS}/experiment_3_significance.csv", index=False)

print(f"\nSignificance results (MAE, Bonferroni alpha = {BONFERRONI_ALPHA_E3:.4f}):")
print(df_sig[df_sig["metric"] == "MAE"]
      [["group_a", "group_b", "p_raw", "p_adjusted", "significant"]]
      .to_string(index=False))


# ── Figure 1: Box plots (MAE, RMSE, R2) ──────────────────────────────────────
sns.set_theme(style="whitegrid")
palette = sns.color_palette("Set2", len(GROUP_NAMES))

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for ax, (metric, ylabel) in zip(
    axes,
    [("mae", "MAE (years)"), ("rmse", "RMSE (years)"), ("r2", "R2")],
):
    data = [
        df_scores[df_scores["group"] == g][metric].values
        for g in GROUP_NAMES
    ]
    short_labels = ["G1\nAnthro\nMetabolic", "G2\n+Bio-\nimpedance",
                    "G3\n+Postural\nRisk", "G4\n+Joint\nAngles"]
    bp = ax.boxplot(
        data,
        labels=short_labels,
        patch_artist=True,
        medianprops={"color": "black", "linewidth": 2},
    )
    for patch, color in zip(bp["boxes"], palette):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)

    ax.set_title(ylabel, fontsize=12, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_xlabel("Feature Group", fontsize=11)

fig.suptitle(
    f"Experiment 3 — Feature Group Ablation ({BEST_MODEL_NAME})\n"
    f"({config.N_CV_SPLITS} GroupShuffleSplits, N = 158 records, "
    f"test_size = {config.TEST_SIZE})",
    fontsize=12,
    y=1.02,
)
plt.tight_layout()
plt.savefig(
    f"{config.DIR_RESULTS}/experiment_3_boxplot.png",
    dpi=150,
    bbox_inches="tight",
)
plt.close()
print("\nBox plot saved.")


# ── Figure 2: Learning curve — mean MAE +/- 95% CI vs feature count ──────────
mae_summary = df_summary[df_summary["metric"] == "MAE"].copy()
mae_summary = mae_summary.set_index("group").loc[GROUP_NAMES].reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
x = mae_summary["n_features"].values
y = mae_summary["mean"].values
ci_lower = mae_summary["ci_lower"].values
ci_upper = mae_summary["ci_upper"].values

ax.plot(x, y, "o-", color="#4c72b0", linewidth=2, markersize=8, label="Mean MAE")
ax.fill_between(x, ci_lower, ci_upper, alpha=0.25, color="#4c72b0", label="95% CI")

for xi, yi, gname in zip(x, y, GROUP_NAMES):
    short = gname.split("_")[0]  # "G1", "G2", etc.
    ax.annotate(short, (xi, yi), textcoords="offset points",
                xytext=(6, 4), fontsize=9)

ax.set_xlabel("Number of features", fontsize=11)
ax.set_ylabel("Mean MAE (years)", fontsize=11)
ax.set_title(
    f"Experiment 3 — MAE vs feature count ({BEST_MODEL_NAME})\n"
    f"Shaded band = 95% CI over {config.N_CV_SPLITS} splits",
    fontsize=11,
)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(
    f"{config.DIR_RESULTS}/experiment_3_learning_curve.png",
    dpi=150,
    bbox_inches="tight",
)
plt.close()
print("Learning curve saved.")

print(f"\nExperiment 3 complete. All outputs in {config.DIR_RESULTS}/")
