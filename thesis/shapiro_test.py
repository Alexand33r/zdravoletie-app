"""
Shapiro-Wilk normality test on per-fold MAE distributions from all three experiments.
Used to justify the choice of Wilcoxon signed-rank (non-parametric) over paired t-test
in the statistical testing section of the thesis.
"""

import sys
import os

import pandas as pd
from scipy.stats import shapiro

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

exp1 = pd.read_csv(os.path.join(RESULTS_DIR, "experiment_1_scores.csv"))
exp2 = pd.read_csv(os.path.join(RESULTS_DIR, "experiment_2_scores.csv"))
exp3 = pd.read_csv(os.path.join(RESULTS_DIR, "experiment_3_scores.csv"))

rows = []

# Experiment 1 — five models
print("=" * 72)
print("EXPERIMENT 1 — per-model MAE across 30 folds")
print("=" * 72)
print(f"{'Condition':<45} {'W':>8} {'p-value':>10} {'Normal?':>10}")
print("-" * 72)

for model in sorted(exp1["model"].unique()):
    scores = exp1.loc[exp1["model"] == model, "mae"].values
    w, p = shapiro(scores)
    label = f"normal (p>=0.05)" if p >= 0.05 else "NON-NORMAL"
    key = f"Exp1 | {model}"
    print(f"{key:<45} {w:>8.4f} {p:>10.4f} {label:>10}")
    rows.append({"condition": key, "W": w, "p": p, "normal": p >= 0.05})

# Experiment 2 — three regimes x five models
print()
print("=" * 72)
print("EXPERIMENT 2 — per-regime/model MAE across 30 folds")
print("=" * 72)
print(f"{'Condition':<45} {'W':>8} {'p-value':>10} {'Normal?':>10}")
print("-" * 72)

for regime in ["RealOnly", "RealPlusSynth", "SynthOnly"]:
    for model in sorted(exp2["model"].unique()):
        mask = (exp2["regime"] == regime) & (exp2["model"] == model)
        scores = exp2.loc[mask, "mae"].values
        w, p = shapiro(scores)
        label = "normal (p>=0.05)" if p >= 0.05 else "NON-NORMAL"
        key = f"Exp2 | {regime} | {model}"
        print(f"{key:<45} {w:>8.4f} {p:>10.4f} {label:>10}")
        rows.append({"condition": key, "W": w, "p": p, "normal": p >= 0.05})

# Experiment 3 — four feature groups (best model: HistGradientBoosting by convention,
# but Exp3 stores only one model's scores per group — confirm)
print()
print("=" * 72)
print("EXPERIMENT 3 — per-feature-group MAE across 30 folds")
print("=" * 72)
print(f"{'Condition':<45} {'W':>8} {'p-value':>10} {'Normal?':>10}")
print("-" * 72)

for group in sorted(exp3["group"].unique()):
    scores = exp3.loc[exp3["group"] == group, "mae"].values
    w, p = shapiro(scores)
    label = "normal (p>=0.05)" if p >= 0.05 else "NON-NORMAL"
    key = f"Exp3 | {group}"
    print(f"{key:<45} {w:>8.4f} {p:>10.4f} {label:>10}")
    rows.append({"condition": key, "W": w, "p": p, "normal": p >= 0.05})

# Summary
total = len(rows)
non_normal = sum(1 for r in rows if not r["normal"])
normal = total - non_normal

print()
print("=" * 72)
print("SUMMARY")
print("=" * 72)
print(f"Total distributions tested : {total}")
print(f"p >= 0.05 (cannot reject normality) : {normal}")
print(f"p <  0.05 (non-normal)              : {non_normal}")
print()
if non_normal > 0:
    print("Non-normal distributions:")
    for r in rows:
        if not r["normal"]:
            print(f"  {r['condition']}  (p={r['p']:.4f})")
print("=" * 72)
