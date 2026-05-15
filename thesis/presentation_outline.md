# Oral Defence Presentation Outline
# Zdravoletie Graduation Project — July 4–5, 2026
# Duration: 15 minutes (+ examiner Q&A)

---

## Slide 1 — Title and Framing (1 min)

**What to show:**
Title: "Reverse-Engineering a Proprietary Health Score from Biometric Inputs"
Subtitle: Comparative evaluation of modelling approaches and synthetic data augmentation
Your name, Fontys UAS, Zdravoletie, July 2026

**What to say:**
This project is not about predicting biological age. The Anovator system computes a score called bodyAge using a formula Zdravoletie practitioners cannot see. The research question is: can machine learning regression models learn to reproduce that formula from its inputs — and if so, which inputs carry the most weight?

**Likely examiner question:** Why is this not biological age prediction?
**One-sentence answer:** Because there is no externally validated ground truth; bodyAge is the Anovator formula's own output, and treating it as a clinical measure of ageing would require mortality or morbidity endpoint data this study does not have.

---

## Slide 2 — Dataset and the Ceiling Effect (1 min)

**What to show:**
- 158 scan records, 53 unique clients, Zdravoletie 2022–2024
- Age gap distribution: histogram or summary statistics (mean 0.45 y, SD 3.30 y, concentrated near zero)
- The GroupShuffleSplit constraint: person-level grouping prevents data leakage

**What to say:**
The target variable is age gap = bodyAge minus chronological age. The distribution is compressed near zero — this is a structural property of the Anovator formula, not a data quality problem, and it sets a practical floor on prediction error. A model that always predicts zero would achieve roughly the mean absolute deviation of the distribution. Any trained regressor has to beat that baseline meaningfully.

**Likely examiner question:** Why not use more data?
**One-sentence answer:** The full Anovator web interface for Zdravoletie yielded 158 records from 53 clients; there is no programmatic API, extraction was manual, and dataset size is the binding constraint throughout the study.

---

## Slide 3 — Experimental Design (1 min)

**What to show:**
Three experiments in one diagram or bullet list:
1. Model comparison — five algorithms, 30 folds, Wilcoxon + Bonferroni
2. Synthetic data ablation — three regimes (RealOnly, RealPlusSynth, SynthOnly)
3. Feature group ablation — four cumulative groups, best model only

Protocol constants: 30 GroupShuffleSplit folds, fixed seed 42, 95% CI from t-distribution, Bonferroni-corrected Wilcoxon throughout.

**What to say:**
All three experiments share the same evaluation protocol. The 30-fold structure with group-based splitting is the methodological backbone of the study. Statistical claims require corrected Wilcoxon significance; everything that does not reach threshold is reported as inconclusive, not equivalent.

**Likely examiner question:** Why Wilcoxon rather than a t-test?
**One-sentence answer:** Per-fold error distributions are non-normal, particularly in folds where the Unknown group dominates the test set, so a non-parametric paired test is more appropriate than a paired t-test.

---

## Slide 4 — Experiment 1: Model Comparison (1.5 min)

**What to show:**
Table: five models ordered by mean MAE with 95% CI
- HistGradientBoosting: 2.43 y [2.09, 2.76]
- Ridge: 2.48 y [2.09, 2.87]
- RandomForest: 2.51 y [2.18, 2.84]
- GradientBoosting: 2.51 y [2.19, 2.84]
- SVR: 2.62 y [2.30, 2.94]

Significance matrix: all ten pairwise comparisons inconclusive (best adjusted p = 0.043, threshold 0.005).

**What to say:**
The key finding is not who won — it is that no one can be declared the winner at this sample size. The CI ranges span 0.65–0.78 years, far larger than the differences between models. The fact that Ridge achieves essentially the same MAE as HistGradientBoosting is substantively interesting: it suggests the predictive information in these 88 features is largely captured by linear combinations, which in turn implies the Anovator formula itself may be approximately linear in the inputs.

**Likely examiner question:** Isn't it a problem that none of your comparisons are significant?
**One-sentence answer:** No — it is an honest finding that characterises the limit of what 53 individuals can establish, and it is reported precisely as statistical indeterminacy rather than being dressed up as something it is not.

---

## Slide 5 — Experiment 2: Synthetic Data Ablation (1.5 min)

**What to show:**
Table or grouped bar chart showing RealOnly vs RealPlusSynth vs SynthOnly MAE for all five models.
Highlight: Ridge SynthOnly = 3.23 y (worst result in the study).
Significant pairs (adjusted p values): HGB, SVR, RF, GB all significant for RealOnly vs RealPlusSynth.

**What to say:**
Synthetic augmentation significantly improves four of five models. The mechanism is interpretable: 1000 GMM-generated records fill gaps in the 53-individual input space, and tree-based methods and kernel SVMs benefit from better coverage. Ridge is the exception — under SynthOnly its MAE rises 30%. The pseudo-labels have a standard deviation of 1.91 years versus 3.30 years in the real targets; linear models calibrate to that compressed range and then underperform on the wider real distribution. This is a clear, falsifiable case study in when synthetic augmentation is contraindicated.

**Likely examiner question:** Why use pseudo-labels at all? Why not just use the real labels for synthetic records?
**One-sentence answer:** Synthetic records have no real labels because they are generated from a distribution, not measured; pseudo-labels from the production model are the only option, and the compression in their variance is an inherent consequence of that approach.

---

## Slide 6 — Experiment 3: Feature Group Ablation (1 min)

**What to show:**
Bar chart or table: G1 (63 features, MAE 2.39 y) through G4 (88 features, MAE 2.43 y).
All six pairwise comparisons inconclusive (lowest raw p = 0.21).
SHAP top features: waist circumference dominant (mean |SHAP| 0.69 y), aerobicGoal, agility, intra-abdominal fat, BMI — all anthropometric/metabolic.

**What to say:**
Adding bioimpedance, postural risk scores, and joint angles to the base feature set produces no statistically significant improvement and a marginal numerical increase in error. The SHAP analysis supports the same conclusion from a different angle: the top predictors are all anthropometric and metabolic, with the first bioimpedance feature appearing at rank five and the first joint angle feature at rank eleven. The implication is that the Anovator formula places minimal weight on those specialist measurement modalities — which is relevant practical information for Zdravoletie, independent of the modelling exercise.

**Likely examiner question:** If G1 is best, why not just use G1 in the dashboard?
**One-sentence answer:** The production dashboard uses the full 88-feature model trained on all 158 records — the ablation result is a finding about the formula's information structure, not a recommendation to discard sensors.

---

## Slide 7 — Streamlit Dashboard Demo (2 min)

**What to show:**
Live demo or screenshots of five pages:
1. Individual Report — client selector, predicted age gap, SHAP bar chart
2. Upload New Scan — CSV upload, prediction, risk/protective factors
3. Population View — histogram + scatter plot with client marked
4. Export PDF — one-page report download
5. About — plain-language limitations text

**What to say:**
The dashboard makes the surrogate model accessible to Zdravoletie practitioners without requiring any data science background. SHAP values on the individual report page translate the model's prediction into a ranked list of which measurements drove the result for that specific client. The About page is explicit about what the tool is not: it does not diagnose, it does not predict health outcomes, and it reflects the Anovator formula rather than clinical biological age.

**Likely examiner question:** Is this deployed?
**One-sentence answer:** Yes, it is live on Streamlit Community Cloud and has been tested end-to-end on the production dataset.

---

## Slide 8 — Conclusions Answering the Sub-Questions (2 min)

**What to show:**
Three bullet answers, one per sub-question:

1. **Best algorithm:** HistGradientBoosting numerically (MAE 2.43 y), but no algorithm can be statistically certified as superior at this sample size — all ten pairwise comparisons are inconclusive.

2. **Synthetic augmentation:** Significantly improves ensemble methods and SVR (adjusted p down to 0.000004). Contraindicated for Ridge under SynthOnly due to pseudo-label variance compression.

3. **Feature groups:** No statistically significant evidence that bioimpedance, postural risk, or joint angles add independent predictive information beyond the 63-feature anthropometric and metabolic base. SHAP values independently confirm this gradient.

**What to say:**
The three answers are honest in a specific way: two of them are partial — they identify a best performer and a direction of effect, but they cannot assert statistical superiority or equivalence. That is the correct characterisation for 53 individuals under Bonferroni correction, and it is more useful than overclaiming.

**Likely examiner question:** What would it take to resolve the inconclusive comparisons?
**One-sentence answer:** Formal power analysis suggests that resolving moderate effect sizes at Bonferroni-corrected alpha with 30 folds would require substantially more than 53 individuals — likely in the range of 150–200 unique clients, which is the first recommendation in the future work section.

---

## Slide 9 — Limitations and Future Work (1 min)

**What to show:**
Four limitations (brief):
1. 53 individuals — statistical power is the binding constraint throughout
2. Unknown group (103 records) — creates distribution shift in folds where it dominates
3. Sentinel values: sportSafeRisk and sportLevel use -1 for missing data, passed as continuous
4. aggregated_postural_index is arithmetically redundant within its feature group

Top future work items:
- Dataset expansion (highest impact)
- Sentinel re-encoding
- CTGAN/copula comparison once N > ~500
- Longitudinal evaluation splits

**What to say:**
The limitations are documented in the methodology chapter and carried through to the discussion and conclusion. None of them are concealed or apologised for — they are the conditions under which this study operates, and the findings are characterised accordingly. The most important future action is straightforward: more data.

**Likely examiner question:** Why was the midterm framing wrong, and how did you catch it?
**One-sentence answer:** The initial framing treated bodyAge as a validated clinical ground truth, which it is not; the educational supervisor identified this at the midterm, and the correction was to reframe the problem as score reverse-engineering using the formula's own output as the target.

---

## Slide 10 — Questions Buffer (2 min)

**What to show:**
Blank or title slide with: "Questions"

**Preparation notes — likely hard questions and one-sentence answers:**

- *"The R² values are all negative — doesn't that mean your model is worse than a mean predictor?"*
  R² on 11–13 test records with SD 3.30 y is extremely noisy; MAE and RMSE are the primary metrics and are reported as such throughout.

- *"You changed the framing mid-project — doesn't that undermine the rigour of the study?"*
  No — the change was made before any experiments were finalised; the corrected framing is more rigorous, not less, because it removes a claim the data cannot support.

- *"Why not tune the hyperparameters? You might get much better results."*
  Hyperparameters are fixed to compare algorithm families, not optimised configurations; tuning is listed as future work and is outside the defined scope.

- *"The Streamlit app predicts age gap for new clients — is that clinically safe to use?"*
  The About page explicitly states it is not a diagnostic tool; it reflects the Anovator formula and should be interpreted alongside the actual scan, not instead of it.

- *"Your GMM fidelity metric shows the synthetic data is close to real — but how do you know the model trained on it learns the right things?"*
  The evaluation is always on real held-out data with real labels; fidelity of the synthetic distribution is a necessary but not sufficient condition, and the actual performance on real test folds is the meaningful criterion.

---

## Timing summary

| Slide | Topic | Time |
|---|---|---|
| 1 | Title and framing | 1 min |
| 2 | Dataset and ceiling effect | 1 min |
| 3 | Experimental design | 1 min |
| 4 | Experiment 1: model comparison | 1.5 min |
| 5 | Experiment 2: synthetic ablation | 1.5 min |
| 6 | Experiment 3: feature group ablation | 1 min |
| 7 | Dashboard demo | 2 min |
| 8 | Conclusions per sub-question | 2 min |
| 9 | Limitations and future work | 1 min |
| 10 | Questions buffer | 2 min |
| **Total** | | **15 min** |
