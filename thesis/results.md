# Chapter 4 — Results

## 4.1 Preliminary Note on R²

All three experiments report mean coefficient of determination (R²) alongside MAE and RMSE for completeness. However, R² must be interpreted with caution in this setting. Each test fold contains between 11 and 13 records. With test sets of this size, R² estimates are extremely noisy: a single outlier prediction can shift the fold-level R² from positive territory into strongly negative values. This instability is reflected in the wide confidence intervals observed throughout — for example, HistGradientBoosting in Experiment 1 achieves a mean R² of −0.36 with a 95% CI of [−0.70, −0.03], a range spanning 0.67 units on a metric whose theoretical maximum is 1.0. All five models return negative mean R² values in the RealOnly regime of Experiment 2, meaning that on average the models' predictions carry higher squared error than a naive constant-mean predictor on these small test folds. This is not an indication that the models are uninformative; it is a consequence of evaluating on 11–13 rows with high outcome variance (age_gap standard deviation = 3.30 years). MAE and RMSE are the primary metrics throughout, as they are more stable under small sample conditions. R² results are reported for completeness and transparency but are not used as the basis for any comparative claims.

## 4.2 Experiment 1: Model Comparison

### 4.2.1 Performance Across Metrics

Table 4.1 presents mean MAE, RMSE, and R² with 95% confidence intervals for all five models, derived from 30 GroupShuffleSplit folds. Models are ordered by ascending mean MAE.

**Table 4.1 — Experiment 1: Mean performance metrics (95% CI) across 30 folds**

| Model | MAE mean | MAE 95% CI | RMSE mean | RMSE 95% CI | R² mean | R² 95% CI |
|---|---|---|---|---|---|---|
| HistGradientBoosting | 2.43 | [2.09, 2.76] | 3.05 | [2.66, 3.44] | −0.36 | [−0.70, −0.03] |
| Ridge | 2.48 | [2.09, 2.87] | 3.10 | [2.62, 3.58] | −0.49 | [−1.06, 0.08] |
| RandomForest | 2.51 | [2.18, 2.84] | 3.20 | [2.85, 3.56] | −0.47 | [−0.77, −0.17] |
| GradientBoosting | 2.51 | [2.19, 2.84] | 3.13 | [2.75, 3.51] | −0.42 | [−0.74, −0.10] |
| SVR | 2.62 | [2.30, 2.94] | 3.42 | [3.11, 3.73] | −0.66 | [−0.91, −0.41] |

HistGradientBoosting achieves the lowest mean MAE at 2.43 years, and the lowest mean RMSE at 3.05 years. SVR has the highest mean MAE at 2.62 years and the highest mean RMSE at 3.42 years, and produces the most consistently negative R² values. Ridge and the two ensemble boosting methods occupy the middle of the ranking. The 95% confidence intervals for MAE overlap extensively across all five models. The confidence interval for Ridge is notably wider than those of the other models (spanning 0.78 years compared to approximately 0.65 years for the others), reflecting higher fold-to-fold variance in Ridge's per-fold MAE scores (standard deviation 1.05 years versus 0.88–0.90 years for the ensemble methods).

### 4.2.2 Statistical Significance

Table 4.2 presents the Wilcoxon signed-rank test results for all ten model pairs on MAE, with Bonferroni-corrected p-values and the corrected significance threshold of 0.005.

**Table 4.2 — Experiment 1: Wilcoxon signed-rank test results for MAE (Bonferroni alpha = 0.005)**

| Model A | Model B | p (raw) | p (adjusted) | Significant |
|---|---|---|---|---|
| SVR | HistGradientBoosting | 0.0043 | 0.0434 | No |
| RandomForest | HistGradientBoosting | 0.0577 | 0.5769 | No |
| RandomForest | SVR | 0.0636 | 0.6356 | No |
| Ridge | SVR | 0.0767 | 0.7672 | No |
| GradientBoosting | HistGradientBoosting | 0.1294 | 1.0000 | No |
| RandomForest | Ridge | 0.2710 | 1.0000 | No |
| Ridge | GradientBoosting | 0.2710 | 1.0000 | No |
| SVR | GradientBoosting | 0.3599 | 1.0000 | No |
| RandomForest | GradientBoosting | 0.8236 | 1.0000 | No |
| Ridge | HistGradientBoosting | 0.9515 | 1.0000 | No |

None of the ten pairwise comparisons reaches the Bonferroni-corrected threshold of 0.005. The closest comparison is SVR versus HistGradientBoosting, with a raw p-value of 0.0043 and an adjusted p-value of 0.0434. All ten results must therefore be characterised as inconclusive: the available data cannot establish whether any two models differ in their ability to approximate the Anovator bodyAge score at the required level of statistical confidence. The practical ranking places HistGradientBoosting first and SVR last by mean MAE, with the three remaining models clustered within 0.04 years of each other, but this ranking does not carry statistical certification.

## 4.3 Experiment 2: Synthetic Data Ablation

### 4.3.1 Performance by Regime and Model

Table 4.3 presents mean MAE with 95% confidence intervals for all five models under each of the three training regimes. All test evaluations use the same real held-out folds with true age_gap labels.

**Table 4.3 — Experiment 2: Mean MAE (95% CI) by model and training regime**

| Model | RealOnly | RealPlusSynth | SynthOnly |
|---|---|---|---|
| HistGradientBoosting | 2.43 [2.09, 2.76] | 2.09 [1.85, 2.32] | 2.07 [1.84, 2.30] |
| GradientBoosting | 2.51 [2.19, 2.84] | 2.15 [1.93, 2.37] | 2.07 [1.85, 2.30] |
| RandomForest | 2.51 [2.18, 2.84] | 2.26 [2.05, 2.47] | 2.17 [1.93, 2.40] |
| Ridge | 2.48 [2.09, 2.87] | 2.39 [2.15, 2.63] | 3.23 [2.14, 4.31] |
| SVR | 2.62 [2.30, 2.94] | 2.28 [2.06, 2.49] | 2.24 [2.02, 2.45] |

Under the RealPlusSynth regime, four of the five models show a reduction in mean MAE relative to RealOnly, with improvements ranging from 0.09 years for Ridge to 0.36 years for HistGradientBoosting. Under the SynthOnly regime, three of the five ensemble models (HistGradientBoosting, GradientBoosting, RandomForest) and SVR show further or comparable reduction in mean MAE relative to RealOnly, while Ridge degrades substantially to a mean MAE of 3.23 years with a confidence interval of [2.14, 4.31] — substantially worse than its RealOnly performance of 2.48 years and representing the single largest deterioration observed across the entire experiment.

The RMSE results follow the same ordinal pattern. Under RealPlusSynth, HistGradientBoosting achieves a mean RMSE of 2.70 years (95% CI [2.46, 2.94]) compared to 3.05 years under RealOnly. Under SynthOnly, Ridge's mean RMSE rises to 3.92 years (95% CI [2.85, 5.00]), while the ensemble models remain in the range of 2.74 to 2.88 years.

### 4.3.2 Statistical Significance

Table 4.4 presents the statistically significant pairwise comparisons from Experiment 2, limited to MAE. Bonferroni correction is applied over three regime pairs per model, yielding a corrected threshold of 0.0167.

**Table 4.4 — Experiment 2: Significant Wilcoxon results for MAE (Bonferroni alpha = 0.0167)**

| Model | Regime A | Regime B | p (raw) | p (adjusted) |
|---|---|---|---|---|
| HistGradientBoosting | RealOnly | RealPlusSynth | < 0.000001 | 0.000004 |
| SVR | RealOnly | RealPlusSynth | 0.000003 | 0.000010 |
| SVR | RealOnly | SynthOnly | 0.000027 | 0.000081 |
| RandomForest | RealOnly | RealPlusSynth | 0.000111 | 0.000332 |
| GradientBoosting | RealOnly | RealPlusSynth | 0.000952 | 0.002855 |

Five comparisons reach significance. For HistGradientBoosting, RandomForest, GradientBoosting, and SVR, the RealOnly versus RealPlusSynth comparison is statistically significant, with adjusted p-values ranging from 0.000004 to 0.002855. For SVR, the RealOnly versus SynthOnly comparison also reaches significance (p_adjusted = 0.000081). No regime pair comparison reaches significance for Ridge. The RealPlusSynth versus SynthOnly comparison is not significant for any model, indicating that the addition of real training records to the synthetic corpus does not produce a detectably different outcome from using the synthetic corpus alone — under the available statistical power.

## 4.4 Experiment 3: Feature Group Ablation

### 4.4.1 Performance by Feature Group

Table 4.5 presents mean MAE, RMSE, and R² with 95% confidence intervals for HistGradientBoosting under each of the four cumulative feature group conditions.

**Table 4.5 — Experiment 3: Mean performance metrics (95% CI) by feature group (HistGradientBoosting)**

| Group | Features | MAE mean | MAE 95% CI | RMSE mean | RMSE 95% CI | R² mean | R² 95% CI |
|---|---|---|---|---|---|---|---|
| G1: Anthropometric + Metabolic | 63 | 2.39 | [2.05, 2.72] | 3.01 | [2.62, 3.40] | −0.33 | [−0.66, −0.01] |
| G2: + Bioimpedance | 73 | 2.42 | [2.07, 2.76] | 3.05 | [2.65, 3.46] | −0.37 | [−0.72, −0.03] |
| G3: + Postural Risk | 83 | 2.42 | [2.08, 2.76] | 3.06 | [2.67, 3.46] | −0.37 | [−0.71, −0.04] |
| G4: + Joint Angles (full) | 88 | 2.43 | [2.09, 2.76] | 3.05 | [2.66, 3.44] | −0.36 | [−0.70, −0.03] |

The anthropometric and metabolic group (G1) achieves the lowest mean MAE at 2.39 years. Each successive addition of a feature group is associated with a marginal increase in mean MAE: adding bioimpedance (G2) raises mean MAE by 0.03 years, adding postural risk (G3) adds a further 0.002 years, and adding joint angles (G4) adds a further 0.006 years. The total difference between the 63-feature group and the full 88-feature set is 0.04 years in mean MAE and 0.04 years in mean RMSE. The confidence intervals for all four groups overlap almost entirely, consistent with the significance test results.

### 4.4.2 Statistical Significance

Table 4.6 presents the Wilcoxon signed-rank test results for all six group pairs on MAE, with Bonferroni-corrected p-values and the corrected significance threshold of 0.0083.

**Table 4.6 — Experiment 3: Wilcoxon signed-rank test results for MAE (Bonferroni alpha = 0.0083)**

| Group A | Group B | p (raw) | p (adjusted) | Significant |
|---|---|---|---|---|
| G1: Anthropometric + Metabolic | G3: + Postural Risk | 0.2207 | 1.0000 | No |
| G1: Anthropometric + Metabolic | G4: + Joint Angles | 0.2129 | 1.0000 | No |
| G1: Anthropometric + Metabolic | G2: + Bioimpedance | 0.2710 | 1.0000 | No |
| G2: + Bioimpedance | G4: + Joint Angles | 0.4280 | 1.0000 | No |
| G3: + Postural Risk | G4: + Joint Angles | 0.5481 | 1.0000 | No |
| G2: + Bioimpedance | G3: + Postural Risk | 0.5699 | 1.0000 | No |

None of the six pairwise comparisons reaches the Bonferroni-corrected threshold of 0.0083. All adjusted p-values are 1.0 after correction, and the lowest raw p-value observed is 0.21. All six comparisons are therefore inconclusive. The data do not support the claim that adding bioimpedance, postural risk, or joint angle features to the anthropometric and metabolic base group produces a statistically distinguishable change in prediction quality.
