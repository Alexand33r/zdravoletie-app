"""
Experiment 2 -- Synthetic Data Ablation
=========================================
Three training regimes compared across five regressors:
  RealOnly       — trained on real data only (true age_gap labels)
  RealPlusSynth  — trained on real + 1000 synthetic rows (pseudo-labels from
                   the production HistGradientBoosting model)
  SynthOnly      — trained on 1000 synthetic rows only (pseudo-labels)

All three regimes are evaluated on the same real-data test folds (true labels).
30 repeated GroupShuffleSplits grouped by individual name. Reports MAE, RMSE,
and R2 as mean +/- 95% CI. Paired Wilcoxon signed-rank tests with Bonferroni
correction (3 regime pairs per model) determine statistical significance.

Pseudo-label rationale: the production model was fit on all 158 real records
via Health_Pipeline.ipynb (teacher). Synthetic data (student) receives its
age_gap labels from that teacher — this is standard knowledge distillation.
Non-significant results must be reported as INCONCLUSIVE, not as evidence
that synthetic augmentation has no effect.

Outputs written to results/:
  experiment_2_scores.csv         per-fold MAE / RMSE / R2 for all models x regimes
  experiment_2_summary.csv        mean, std, 95% CI bounds per model x regime x metric
  experiment_2_significance.csv   Wilcoxon statistics and Bonferroni-adjusted p-values
  experiment_2_boxplot.png        MAE box plots grouped by model (3 regimes per model)
  experiment_2_delta_plot.png     mean MAE delta vs RealOnly (+/-  95% CI) per model

Usage:
  python Experiment_2.py
"""

import json
import warnings
from itertools import combinations
from pathlib import Path

import joblib
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

REGIMES = ["RealOnly", "RealPlusSynth", "SynthOnly"]
N_REGIME_PAIRS = 3  # C(3,2)
BONFERRONI_ALPHA_E2 = config.ALPHA / N_REGIME_PAIRS  # 0.05 / 3 ≈ 0.0167

Path(config.DIR_RESULTS).mkdir(exist_ok=True)

# ── Load real data ────────────────────────────────────────────────────────────
print("Loading real data...")
df = pd.read_csv(config.PATH_MASTER_CSV)

with open(config.PATH_MODEL_FEATURES) as f:
    model_features = json.load(f)

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

print(f"  Real dataset: {len(df)} records, {df[config.GROUP_COLUMN].nunique()} individuals")

# ── Load synthetic data and generate pseudo-labels ───────────────────────────
print("Loading synthetic data and generating pseudo-labels...")
df_synth = pd.read_csv(config.PATH_SYNTHETIC_CSV)

# Synthetic CSV already contains derived features (sex_encoded, muscle_fat_ratio,
# upper_lower_muscle_ratio, trunk_limb_fat_ratio, aggregated_postural_index).
# All 88 model features are present; no missing values in synthetic data.
X_synth = df_synth[model_features].copy()

prod_model  = joblib.load(config.PATH_MODEL)
prod_scaler = joblib.load(config.PATH_SCALER)

X_synth_prod_sc = prod_scaler.transform(X_synth)
y_synth = prod_model.predict(X_synth_prod_sc)

print(f"  Synthetic dataset: {len(df_synth)} rows")
print(f"  Pseudo-labels — mean={y_synth.mean():.2f}  std={y_synth.std():.2f}")


# ── Model factory ─────────────────────────────────────────────────────────────
def make_models() -> dict:
    hp = config.MODEL_HYPERPARAMS
    return {
        "RandomForest":         RandomForestRegressor(**hp["RandomForest"]),
        "Ridge":                Ridge(**hp["Ridge"]),
        "SVR":                  SVR(**hp["SVR"]),
        "GradientBoosting":     GradientBoostingRegressor(**hp["GradientBoosting"]),
        "HistGradientBoosting": HistGradientBoostingRegressor(**hp["HistGradientBoosting"]),
    }


# ── Cross-validation loop ─────────────────────────────────────────────────────
print(f"\nRunning {config.N_CV_SPLITS} GroupShuffleSplits x {len(REGIMES)} regimes...")

gss = GroupShuffleSplit(
    n_splits=config.N_CV_SPLITS,
    test_size=config.TEST_SIZE,
    random_state=config.RANDOM_SEED,
)

records = []

for split_index, (train_idx, test_idx) in enumerate(gss.split(X_full, y_full, groups=groups)):
    X_train_real = X_full.iloc[train_idx].copy()
    X_test_real  = X_full.iloc[test_idx].copy()
    y_train_real = y_full.iloc[train_idx].values
    y_test_real  = y_full.iloc[test_idx].values

    # Impute with training-fold medians (real data only)
    fold_medians = X_train_real.median()
    X_train_real = X_train_real.fillna(fold_medians).fillna(0)
    X_test_real  = X_test_real.fillna(fold_medians).fillna(0)

    for regime in REGIMES:
        if regime == "RealOnly":
            X_tr = X_train_real.values
            y_tr = y_train_real

        elif regime == "RealPlusSynth":
            # Concatenate imputed real training + synthetic (no missing in synth)
            X_tr = np.vstack([X_train_real.values, X_synth.values])
            y_tr = np.concatenate([y_train_real, y_synth])

        else:  # SynthOnly
            X_tr = X_synth.values
            y_tr = y_synth

        # Scale: fit on this regime's training set, transform both train and test
        scaler = StandardScaler()
        X_tr_sc   = scaler.fit_transform(X_tr)
        X_test_sc = scaler.transform(X_test_real.values)

        for model_name, model in make_models().items():
            model.fit(X_tr_sc, y_tr)
            y_pred = model.predict(X_test_sc)

            records.append({
                "split":   split_index,
                "regime":  regime,
                "model":   model_name,
                "mae":     mean_absolute_error(y_test_real, y_pred),
                "rmse":    np.sqrt(mean_squared_error(y_test_real, y_pred)),
                "r2":      r2_score(y_test_real, y_pred),
                "n_test":  len(y_test_real),
            })

    if (split_index + 1) % 5 == 0:
        print(f"  Split {split_index + 1:2d} / {config.N_CV_SPLITS} done")

df_scores = pd.DataFrame(records)
df_scores.to_csv(f"{config.DIR_RESULTS}/experiment_2_scores.csv", index=False)
print(f"\nPer-fold scores saved ({len(df_scores)} rows).")


# ── Summary statistics with 95% CI ───────────────────────────────────────────
t_crit = stats.t.ppf((1 + config.CONFIDENCE_LEVEL) / 2, df=config.N_CV_SPLITS - 1)

summary_rows = []
for regime in REGIMES:
    for model_name in config.MODEL_NAMES:
        subset = df_scores[(df_scores["regime"] == regime) & (df_scores["model"] == model_name)]
        for metric in ["mae", "rmse", "r2"]:
            values  = subset[metric].values
            mean_v  = values.mean()
            std_v   = values.std(ddof=1)
            ci_half = t_crit * std_v / np.sqrt(config.N_CV_SPLITS)
            summary_rows.append({
                "regime":   regime,
                "model":    model_name,
                "metric":   metric.upper(),
                "mean":     round(mean_v,  4),
                "std":      round(std_v,   4),
                "ci_lower": round(mean_v - ci_half, 4),
                "ci_upper": round(mean_v + ci_half, 4),
            })

df_summary = pd.DataFrame(summary_rows)
df_summary.to_csv(f"{config.DIR_RESULTS}/experiment_2_summary.csv", index=False)

print("\nSummary (MAE by regime):")
mae_summary = df_summary[df_summary["metric"] == "MAE"].pivot_table(
    index="model", columns="regime", values="mean"
)[REGIMES]
print(mae_summary.to_string())


# ── Wilcoxon tests: compare regimes within each model ────────────────────────
# 3 regime pairs per model; Bonferroni over 3 pairs (per-model correction).
sig_rows = []
regime_pairs = list(combinations(REGIMES, 2))

for metric in ["mae", "rmse", "r2"]:
    for model_name in config.MODEL_NAMES:
        subset = df_scores[df_scores["model"] == model_name]
        pivot  = subset.pivot(index="split", columns="regime", values=metric)
        for regime_a, regime_b in regime_pairs:
            statistic, p_raw = stats.wilcoxon(
                pivot[regime_a].values,
                pivot[regime_b].values,
                alternative="two-sided",
            )
            p_adjusted = min(p_raw * N_REGIME_PAIRS, 1.0)
            sig_rows.append({
                "metric":        metric.upper(),
                "model":         model_name,
                "regime_a":      regime_a,
                "regime_b":      regime_b,
                "wilcoxon_stat": round(statistic, 3),
                "p_raw":         round(p_raw,      6),
                "p_adjusted":    round(p_adjusted,  6),
                "significant":   p_adjusted < BONFERRONI_ALPHA_E2,
            })

df_sig = pd.DataFrame(sig_rows)
df_sig.to_csv(f"{config.DIR_RESULTS}/experiment_2_significance.csv", index=False)

print(f"\nSignificance results (MAE, Bonferroni alpha = {BONFERRONI_ALPHA_E2:.4f}):")
print(df_sig[df_sig["metric"] == "MAE"]
      [["model", "regime_a", "regime_b", "p_raw", "p_adjusted", "significant"]]
      .to_string(index=False))


# ── Figure 1: Grouped box plots (MAE, RMSE, R2) ──────────────────────────────
sns.set_theme(style="whitegrid")
regime_palette = {"RealOnly": "#4c72b0", "RealPlusSynth": "#55a868", "SynthOnly": "#c44e52"}
model_order = config.MODEL_NAMES

fig, axes = plt.subplots(1, 3, figsize=(20, 7))

for ax, (metric, ylabel) in zip(
    axes,
    [("mae", "MAE (years)"), ("rmse", "RMSE (years)"), ("r2", "R2")],
):
    plot_data = df_scores[["model", "regime", metric]].copy()
    plot_data.columns = ["model", "regime", "value"]

    # Boxplot grouped by model, coloured by regime
    positions = []
    data_groups = []
    colors = []
    tick_positions = []
    tick_labels = []
    group_gap = 1.0
    regime_width = 0.6
    n_regimes = len(REGIMES)

    for i, model_name in enumerate(model_order):
        group_center = i * (n_regimes * regime_width + group_gap)
        tick_positions.append(group_center + (n_regimes - 1) * regime_width / 2)
        tick_labels.append(model_name)
        for j, regime in enumerate(REGIMES):
            pos = group_center + j * regime_width
            positions.append(pos)
            vals = plot_data[(plot_data["model"] == model_name) &
                             (plot_data["regime"] == regime)]["value"].values
            data_groups.append(vals)
            colors.append(regime_palette[regime])

    bp = ax.boxplot(
        data_groups,
        positions=positions,
        widths=regime_width * 0.8,
        patch_artist=True,
        medianprops={"color": "black", "linewidth": 1.5},
    )
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)

    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=30, ha="right", fontsize=9)
    ax.set_title(ylabel, fontsize=12, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_xlabel("Model", fontsize=11)

# Legend
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, fc=regime_palette[r], alpha=0.8, label=r)
    for r in REGIMES
]
fig.legend(handles=legend_handles, loc="upper right", fontsize=10,
           title="Training regime", title_fontsize=10)

fig.suptitle(
    f"Experiment 2 — Synthetic Data Ablation\n"
    f"({config.N_CV_SPLITS} GroupShuffleSplits, N = 158 real records, "
    f"1000 synthetic rows, test_size = {config.TEST_SIZE})",
    fontsize=12,
    y=1.02,
)
plt.tight_layout()
plt.savefig(
    f"{config.DIR_RESULTS}/experiment_2_boxplot.png",
    dpi=150,
    bbox_inches="tight",
)
plt.close()
print("\nBox plot saved.")


# ── Figure 2: MAE delta vs RealOnly (+/- 95% CI) ─────────────────────────────
# Shows whether each regime improves (negative delta) or hurts (positive delta)
# relative to the RealOnly baseline for each model.
mae_df = df_summary[df_summary["metric"] == "MAE"].copy()
real_only_means = mae_df[mae_df["regime"] == "RealOnly"].set_index("model")["mean"]

delta_rows = []
for regime in ["RealPlusSynth", "SynthOnly"]:
    sub = mae_df[mae_df["regime"] == regime].copy()
    for _, row in sub.iterrows():
        baseline = real_only_means[row["model"]]
        delta = row["mean"] - baseline
        ci_half = (row["ci_upper"] - row["ci_lower"]) / 2
        delta_rows.append({
            "regime": regime,
            "model":  row["model"],
            "delta":  delta,
            "ci_half": ci_half,
        })

df_delta = pd.DataFrame(delta_rows)

fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(config.MODEL_NAMES))
width = 0.35
regime_colors = {"RealPlusSynth": "#55a868", "SynthOnly": "#c44e52"}

for i, regime in enumerate(["RealPlusSynth", "SynthOnly"]):
    sub = df_delta[df_delta["regime"] == regime]
    offsets = x + (i - 0.5) * width
    ax.bar(offsets, sub["delta"], width, label=regime,
           color=regime_colors[regime], alpha=0.8)
    ax.errorbar(offsets, sub["delta"], yerr=sub["ci_half"],
                fmt="none", color="black", capsize=4, linewidth=1.2)

ax.axhline(0, color="black", linewidth=1, linestyle="--")
ax.set_xticks(x)
ax.set_xticklabels(config.MODEL_NAMES, rotation=30, ha="right")
ax.set_ylabel("MAE delta vs RealOnly (years)", fontsize=11)
ax.set_title(
    "Experiment 2 — MAE change relative to RealOnly baseline\n"
    "Negative = improvement over real-only; Positive = degradation",
    fontsize=11,
)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(
    f"{config.DIR_RESULTS}/experiment_2_delta_plot.png",
    dpi=150,
    bbox_inches="tight",
)
plt.close()
print("Delta plot saved.")

print(f"\nExperiment 2 complete. All outputs in {config.DIR_RESULTS}/")
