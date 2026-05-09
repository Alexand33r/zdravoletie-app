"""
Experiment 1 -- Model Comparison with Statistical Significance
==============================================================
Five regressors trained on real Anovator data with 30 repeated
GroupShuffleSplits grouped by individual name. Reports MAE, RMSE,
and R2 as mean +/- 95% CI. Paired Wilcoxon signed-rank tests with
Bonferroni correction determine statistical significance.

Framing: models are compared on their ability to reverse-engineer
Anovator's proprietary bodyAge score (expressed as age_gap = bodyAge - age)
from raw biometric inputs.

Outputs written to results/:
  experiment_1_scores.csv         per-fold MAE / RMSE / R2 for all models
  experiment_1_summary.csv        mean, std, 95% CI bounds per model/metric
  experiment_1_significance.csv   Wilcoxon statistics and Bonferroni-adjusted p-values
  experiment_1_boxplot.png        MAE / RMSE / R2 box plots side by side
  experiment_1_sig_matrix.png     significance matrix heatmap for MAE

Usage:
  python Experiment_1.py
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
from sklearn.ensemble import (
    GradientBoostingRegressor,
    HistGradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

import config

warnings.filterwarnings("ignore")
np.random.seed(config.RANDOM_SEED)

# ── Output directory ──────────────────────────────────────────────────────────
Path(config.DIR_RESULTS).mkdir(exist_ok=True)

# ── Data loading ──────────────────────────────────────────────────────────────
print("Loading data...")
df = pd.read_csv(config.PATH_MASTER_CSV)

with open(config.PATH_MODEL_FEATURES) as f:
    model_features = json.load(f)

# ── Feature engineering ───────────────────────────────────────────────────────
# Must match Health_Pipeline.ipynb exactly.
# +0.1 guards prevent division by zero; lowerBody has 47 NaN rows that become
# the training-fold median before this ratio is computed.
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
print(f"  Features: {len(model_features)}")
print(f"  Target: age_gap  mean={y_full.mean():.2f}  std={y_full.std():.2f}")


# ── Model factory ─────────────────────────────────────────────────────────────
def make_models() -> dict:
    """Return fresh model instances using hyperparameters from config."""
    hp = config.MODEL_HYPERPARAMS
    return {
        "RandomForest":         RandomForestRegressor(**hp["RandomForest"]),
        "Ridge":                Ridge(**hp["Ridge"]),
        "SVR":                  SVR(**hp["SVR"]),
        "GradientBoosting":     GradientBoostingRegressor(**hp["GradientBoosting"]),
        "HistGradientBoosting": HistGradientBoostingRegressor(**hp["HistGradientBoosting"]),
    }


# ── Cross-validation loop ─────────────────────────────────────────────────────
print(f"\nRunning {config.N_CV_SPLITS} GroupShuffleSplits...")

gss = GroupShuffleSplit(
    n_splits=config.N_CV_SPLITS,
    test_size=config.TEST_SIZE,
    random_state=config.RANDOM_SEED,
)

records = []

for split_index, (train_idx, test_idx) in enumerate(gss.split(X_full, y_full, groups=groups)):
    X_train = X_full.iloc[train_idx].copy()
    X_test  = X_full.iloc[test_idx].copy()
    y_train = y_full.iloc[train_idx]
    y_test  = y_full.iloc[test_idx]

    # Impute with training-fold medians (computed fresh per split, not from saved file)
    fold_medians = X_train.median()
    X_train = X_train.fillna(fold_medians).fillna(0)
    X_test  = X_test.fillna(fold_medians).fillna(0)

    # Scale: fit on training fold only
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    for model_name, model in make_models().items():
        model.fit(X_train_sc, y_train)
        y_pred = model.predict(X_test_sc)

        records.append({
            "split":  split_index,
            "model":  model_name,
            "mae":    mean_absolute_error(y_test, y_pred),
            "rmse":   np.sqrt(mean_squared_error(y_test, y_pred)),
            "r2":     r2_score(y_test, y_pred),
            "n_test": len(y_test),
        })

    if (split_index + 1) % 5 == 0:
        print(f"  Split {split_index + 1:2d} / {config.N_CV_SPLITS} done  "
              f"(test rows: {len(test_idx)}, "
              f"test individuals: {groups.iloc[test_idx].nunique()})")

df_scores = pd.DataFrame(records)
df_scores.to_csv(f"{config.DIR_RESULTS}/experiment_1_scores.csv", index=False)
print(f"\nPer-fold scores saved ({len(df_scores)} rows).")


# ── Summary statistics with 95% CI ───────────────────────────────────────────
t_crit = stats.t.ppf((1 + config.CONFIDENCE_LEVEL) / 2, df=config.N_CV_SPLITS - 1)

summary_rows = []
for model_name in config.MODEL_NAMES:
    subset = df_scores[df_scores["model"] == model_name]
    for metric in ["mae", "rmse", "r2"]:
        values  = subset[metric].values
        mean_v  = values.mean()
        std_v   = values.std(ddof=1)
        ci_half = t_crit * std_v / np.sqrt(config.N_CV_SPLITS)
        summary_rows.append({
            "model":    model_name,
            "metric":   metric.upper(),
            "mean":     round(mean_v,  4),
            "std":      round(std_v,   4),
            "ci_lower": round(mean_v - ci_half, 4),
            "ci_upper": round(mean_v + ci_half, 4),
        })

df_summary = pd.DataFrame(summary_rows)
df_summary.to_csv(f"{config.DIR_RESULTS}/experiment_1_summary.csv", index=False)

print("\nSummary (MAE):")
print(df_summary[df_summary["metric"] == "MAE"]
      .sort_values("mean")
      .to_string(index=False))


# ── Wilcoxon signed-rank tests with Bonferroni correction ────────────────────
sig_rows = []
model_pairs = list(combinations(config.MODEL_NAMES, 2))

for metric in ["mae", "rmse", "r2"]:
    pivot = df_scores.pivot(index="split", columns="model", values=metric)
    for model_a, model_b in model_pairs:
        statistic, p_raw = stats.wilcoxon(
            pivot[model_a].values,
            pivot[model_b].values,
            alternative="two-sided",
        )
        p_adjusted = min(p_raw * config.N_MODEL_PAIRS, 1.0)  # Bonferroni, capped at 1
        sig_rows.append({
            "metric":        metric.upper(),
            "model_a":       model_a,
            "model_b":       model_b,
            "wilcoxon_stat": round(statistic, 3),
            "p_raw":         round(p_raw,      6),
            "p_adjusted":    round(p_adjusted,  6),
            "significant":   p_adjusted < config.BONFERRONI_ALPHA,
        })

df_sig = pd.DataFrame(sig_rows)
df_sig.to_csv(f"{config.DIR_RESULTS}/experiment_1_significance.csv", index=False)

print(f"\nSignificance results (MAE, Bonferroni alpha = {config.BONFERRONI_ALPHA}):")
print(df_sig[df_sig["metric"] == "MAE"]
      [["model_a", "model_b", "p_raw", "p_adjusted", "significant"]]
      .to_string(index=False))


# ── Figure 1: Box plots (MAE, RMSE, R2) ──────────────────────────────────────
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
palette = sns.color_palette("Set2", len(config.MODEL_NAMES))

for ax, (metric, ylabel) in zip(
    axes,
    [("mae", "MAE (years)"), ("rmse", "RMSE (years)"), ("r2", "R2")],
):
    data = [
        df_scores[df_scores["model"] == m][metric].values
        for m in config.MODEL_NAMES
    ]
    bp = ax.boxplot(
        data,
        labels=config.MODEL_NAMES,
        patch_artist=True,
        medianprops={"color": "black", "linewidth": 2},
    )
    for patch, color in zip(bp["boxes"], palette):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)

    ax.set_title(ylabel, fontsize=12, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_xlabel("Model", fontsize=11)
    ax.tick_params(axis="x", rotation=30)

fig.suptitle(
    f"Experiment 1 — Model Comparison on Real Anovator Data\n"
    f"({config.N_CV_SPLITS} GroupShuffleSplits, "
    f"N = 158 records, 53 individuals, test_size = {config.TEST_SIZE})",
    fontsize=12,
    y=1.02,
)
plt.tight_layout()
plt.savefig(
    f"{config.DIR_RESULTS}/experiment_1_boxplot.png",
    dpi=150,
    bbox_inches="tight",
)
plt.close()
print("\nBox plot saved.")


# ── Figure 2: Significance matrix (MAE) ──────────────────────────────────────
mae_sig = df_sig[df_sig["metric"] == "MAE"]

# Build square matrices for annotation and colour
annot_matrix = pd.DataFrame("", index=config.MODEL_NAMES, columns=config.MODEL_NAMES)
color_matrix  = pd.DataFrame(np.nan, index=config.MODEL_NAMES, columns=config.MODEL_NAMES)

for _, row in mae_sig.iterrows():
    a, b = row["model_a"], row["model_b"]
    label = f"p={row['p_adjusted']:.4f}"
    if row["significant"]:
        label += " *"
    annot_matrix.loc[a, b] = label
    annot_matrix.loc[b, a] = label
    # 1 = significant (green), 0 = inconclusive (light grey)
    color_matrix.loc[a, b] = float(row["significant"])
    color_matrix.loc[b, a] = float(row["significant"])

# Diagonal: blank
for m in config.MODEL_NAMES:
    annot_matrix.loc[m, m] = ""

fig, ax = plt.subplots(figsize=(9, 7))
cmap = plt.cm.get_cmap("RdYlGn", 2)  # 2 discrete colours: red(0)=inconclusive, green(1)=significant

sns.heatmap(
    color_matrix.astype(float),
    annot=annot_matrix,
    fmt="",
    cmap=cmap,
    linewidths=1,
    linecolor="white",
    ax=ax,
    cbar=False,
    vmin=0,
    vmax=1,
    mask=color_matrix.isna(),
)

ax.set_title(
    f"Wilcoxon Significance Matrix -- MAE\n"
    f"Bonferroni-adjusted p-values  |  threshold = {config.BONFERRONI_ALPHA}\n"
    f"Green (*) = significant  |  Red = inconclusive",
    fontsize=11,
)
ax.set_xlabel("Model", fontsize=11)
ax.set_ylabel("Model", fontsize=11)
plt.tight_layout()
plt.savefig(
    f"{config.DIR_RESULTS}/experiment_1_sig_matrix.png",
    dpi=150,
    bbox_inches="tight",
)
plt.close()
print("Significance matrix saved.")

print(f"\nExperiment 1 complete. All outputs in {config.DIR_RESULTS}/")
