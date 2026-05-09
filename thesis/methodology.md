# Chapter 3 — Methodology

## 3.1 Thesis Framing and Research Objective

This project does not aim to predict biological age in the general sense. Its specific objective is to reverse-engineer and analyse Anovator's proprietary bodyAge score from raw biometric inputs, and to evaluate three dimensions of that modelling problem: which regression algorithm best approximates the score, whether Gaussian Mixture Model synthetic data augmentation improves approximation quality, and which biometric feature groups carry the most predictive information relative to the score. Framing the work in terms of score reverse-engineering rather than biological age prediction is important because the ground truth used throughout is bodyAge itself, not an independently validated clinical measure. Every design choice in the experimental pipeline follows from this framing.

## 3.2 Dataset

### 3.2.1 Source and Collection

All data originate from Anovator body scan sessions conducted at Zdravoletie, a health and rehabilitation centre in Bulgaria. Records were collected between 2022 and 2024 using the Anovator scanning platform, which combines impedance bioelectrical analysis, postural camera imaging, and manual biometric measurements administered by clinic staff. The dataset comprises 158 individual scan records drawn from 53 unique clients. Each client may appear in multiple records across different sessions. The dataset was assembled manually from the Anovator web interface; no public data sources were combined with it.

### 3.2.2 Target Variable

Anovator computes a proprietary score called bodyAge for each scan. The target variable throughout all experiments is the age gap, defined as the signed difference between bodyAge and the client's chronological age at the time of the scan:

    age_gap = bodyAge - age

A positive age_gap indicates that the Anovator system judged the client's biological condition to be older than their chronological age; a negative value indicates the reverse. Across the 158 records, age_gap has a mean of 0.45 years and a standard deviation of 3.30 years. The models in this study learn to predict age_gap rather than bodyAge directly, which removes the confounding effect of chronological age from the target distribution and makes the prediction task conceptually equivalent to reverse-engineering the deviation component of the Anovator formula.

### 3.2.3 Feature Set

The final model feature set comprises 88 variables derived from the raw Anovator outputs. These were determined during exploratory analysis and model training in the Health_Pipeline.ipynb notebook and are loaded at runtime from a stored JSON artifact (models/model_features.json). The 88 features decompose into four groups used in Experiment 3:

Sixty-three features constitute the anthropometric and metabolic group, which includes body composition measurements (weight, height, BMI, body fat percentage, muscle mass, bone mass, protein content, water content, subcutaneous fat, intra-abdominal fat, and segmental decompositions thereof), Anovator-computed health goal recommendations (aerobic goal, anaerobic goal, caloric input target, weight control, fat control, and muscle control targets), balance and agility scores, vital signs recorded where available (blood oxygen saturation, resting heart rate, blood pressure), optional clinical measurements (vision acuity, vital lung capacity), body shape classification, fitness assessments (heart function score), and demographic features (chronological age and sex, the latter encoded as a binary variable).

Ten bioimpedance features form the second group: raw impedance measurements at 20 kHz and 100 kHz for each of the four limbs and the trunk (r20LeftArm, r20RightArm, r20LeftLeg, r20RightLeg, r20Trunk, r100LeftArm, r100RightArm, r100LeftLeg, r100RightLeg, r100Trunk). These reflect the electrical properties of tissue at different frequencies and are used in bioelectrical impedance analysis to estimate body composition.

Ten postural risk features constitute the third group, comprising camera-based postural risk scores: frontHeadRisk, headRisk, humpbackRisk, kneeRisk, pelvisRisk, postureRisk, shoulderRisk, spineRisk, side_hunchback_risk, and a derived feature aggregated_postural_index, which is the arithmetic mean of six of these component scores (see Section 3.8 for the limitation this introduces).

Five joint angle features form the fourth group: front_shoulder_angle, front_left_leg_angle, front_right_leg_angle, side_left_leg_angle, and side_right_leg_angle, all extracted from Anovator's postural camera analysis.

## 3.3 Feature Engineering

Five derived features are computed from raw columns and are included in the model feature set. Sex is encoded as a binary integer (0 for female, 1 for male). Three body composition ratios are computed: muscle-to-fat ratio (muscle divided by fat plus 0.1), upper-to-lower body muscle ratio (upperBody divided by lowerBody plus 0.1), and trunk-to-limb fat ratio (fatTrunk divided by the sum of the four limb fat measurements plus 0.1). The additive constant of 0.1 in each denominator prevents division by zero and is applied consistently in all three experiments, in the Streamlit dashboard inference code, and in the synthetic data generation pipeline to ensure numerical consistency across contexts. The aggregated_postural_index is the mean of humpbackRisk, spineRisk, pelvisRisk, postureRisk, kneeRisk, and frontHeadRisk. Following feature engineering, any infinite values produced by division operations are replaced with missing values (NaN), which are then handled at the imputation stage.

All feature engineering is applied to the full dataset before the cross-validation loop in each experiment. The synthetic dataset used in Experiment 2 already contains all five derived features in pre-computed form, because they were included in the GMM training distribution.

## 3.4 Cross-Validation Protocol

### 3.4.1 Group-based Splitting

All three experiments use GroupShuffleSplit from scikit-learn with the grouping variable set to the client name field. This prevents data leakage at the person level: when a client has multiple scan records across different sessions, all of that client's records are assigned together to either the training fold or the test fold in a given split. Without this constraint, a model could exploit within-person consistency — learning the stable biometric profile of an individual — rather than generalising across individuals, which would inflate performance estimates beyond what the model could achieve on genuinely unseen clients.

Each split assigns 80% of the 53 unique individuals to training and 20% to test, yielding approximately 11 to 13 test records per split. The split is non-exhaustive and repeated 30 times, consistent with established practice for repeated random sub-sampling cross-validation. The test size and split count are fixed across all three experiments to ensure comparability. All splits use a fixed random seed of 42.

### 3.4.2 Imputation and Scaling

Missing values are imputed using the median of the training fold in each split. This median is computed fresh from the training fold after the split is drawn and is not imported from any stored artifact. A secondary fillna(0) handles the rare case where a feature is entirely missing from the training fold and thus has no computable median. The test fold is then imputed using the same training-fold medians — ensuring that no information from the test set informs the imputation. This procedure is applied in all three experiments.

StandardScaler is fit on the training fold after imputation and applied to both training and test folds. As with imputation, the scaler is fit fresh for each split and never shared across folds. In Experiment 2, the scaler is fit on the training data appropriate to each regime: the real training fold alone for the RealOnly condition, the concatenated real and synthetic training data for RealPlusSynth, and the full synthetic dataset for SynthOnly.

## 3.5 Experiment 1: Model Comparison

Experiment 1 evaluates five regression algorithms on their ability to predict age_gap from the full 88-feature set: RandomForestRegressor, Ridge, SVR (radial basis function kernel), GradientBoostingRegressor, and HistGradientBoostingRegressor. All models use scikit-learn implementations with fixed hyperparameters specified in a central configuration module. RandomForest uses 100 estimators with maximum depth capped at 7 to limit overfitting on the approximately 145 training rows available per split. Ridge uses a regularisation coefficient of 1.0. SVR uses a radial basis function kernel with C=1.0 and epsilon=0.1. GradientBoosting uses 100 estimators with learning rate 0.1 and maximum depth 3. HistGradientBoosting uses 100 maximum iterations. No hyperparameter search is performed; the values represent defensible defaults appropriate to the training set size and are held fixed across all three experiments.

For each of the 30 splits, fresh model instances are instantiated, trained on the scaled training fold, and evaluated on the scaled test fold. Mean absolute error, root mean squared error, and coefficient of determination (R²) are recorded for each model in each split, yielding 30 paired observations per model across each metric. Summary statistics (mean, standard deviation, and 95% confidence interval) are computed using the t-distribution with 29 degrees of freedom.

## 3.6 Experiment 2: Synthetic Data Ablation

Experiment 2 investigates whether augmenting the training set with Gaussian Mixture Model synthetic data improves prediction of age_gap on real held-out data. Three training regimes are evaluated for each of the five models:

The RealOnly regime trains exclusively on the real records assigned to the training fold in each split. The RealPlusSynth regime augments the real training fold with all 1000 synthetic records before training. The SynthOnly regime trains exclusively on the 1000 synthetic records and evaluates on the real test fold without any real training data.

The 1000-record synthetic dataset was generated by fitting a Gaussian Mixture Model with five components and full covariance matrices to the 158 real records in Data_Gen.ipynb. Because the synthetic records do not carry a ground-truth age_gap value — the Anovator score cannot be synthesised — pseudo-labels are generated by applying the production model (trained on all 158 real records in Health_Pipeline.ipynb) to the synthetic feature vectors. This constitutes a teacher-student knowledge distillation setup: the production model serves as the teacher, and the synthetic records serve as an unlabelled student corpus that receives soft labels from the teacher's predictions. The pseudo-labels have a mean of 0.75 years and a standard deviation of 1.91 years, compared to the real label distribution of mean 0.45 years and standard deviation 3.30 years. This compression of the label variance is a structural consequence of the regression model's tendency to predict toward the mean and has implications for linear models that are discussed in Chapter 5.

In all three regimes, the test fold is always the same real-data held-out set with true age_gap labels. The same 30-split GroupShuffleSplit schedule is used, applied only to the real data. The synthetic records are not subject to the group constraint.

## 3.7 Experiment 3: Feature Group Ablation

Experiment 3 evaluates the marginal contribution of each biometric feature group to prediction quality, using HistGradientBoosting as the sole model. HistGradientBoosting was selected because it achieved the lowest mean MAE in Experiment 1 (2.43 years, 95% CI [2.09, 2.76]). The feature groups are evaluated cumulatively in the following order:

Group 1 (63 features) comprises the anthropometric and metabolic features. Group 2 (73 features) adds the ten bioimpedance measurements to Group 1. Group 3 (83 features) further adds the ten postural risk scores. Group 4 (88 features) adds the five joint angle measurements, completing the full model feature set.

This additive structure allows inference about the marginal predictive value of each feature category beyond what the preceding groups already contribute. The same 30-split protocol, imputation procedure, and scaling procedure apply. Because only one model is evaluated, the number of Wilcoxon test pairs is C(4,2) = 6.

## 3.8 Statistical Testing

Pairwise statistical significance is assessed using the Wilcoxon signed-rank test, which is appropriate for paired, non-normally distributed observations. In Experiment 1, each of the C(5,2) = 10 model pairs yields a signed-rank test on 30 paired fold scores per metric. The Bonferroni correction is applied over the 10 pairs, yielding a corrected significance threshold of alpha = 0.005. In Experiment 2, regime pairs are tested within each model: three pairs per model over 30 fold observations, with a per-model Bonferroni correction yielding a threshold of alpha / 3 ≈ 0.0167. In Experiment 3, six group pairs are tested over 30 fold observations, with a Bonferroni correction yielding a threshold of alpha / 6 ≈ 0.0083.

A result that does not reach the corrected significance threshold must be characterised as inconclusive rather than as evidence of equivalence. With 30 paired observations and a corrected threshold well below the nominal 0.05 level, the tests have limited statistical power to detect moderate effect sizes. This constraint is structural and is a direct consequence of the dataset size (53 unique individuals). It is addressed in full in Section 3.9.4 and in the discussion chapter.

## 3.9 Known Limitations of the Dataset and Feature Set

The following four limitations were identified during a pre-experiment validation pass and are stated explicitly here. They do not invalidate the experiments but bear on the interpretation of results and must be acknowledged at oral defence.

### 3.9.1 Sentinel Values Encoded as Numeric Features

Two features use the integer -1 as a machine sentinel meaning that the metric was not computed for a given scan: sportSafeRisk is -1 in 37% of records (approximately 58 of 158), and sportLevel is -1 in 70% of records (approximately 111 of 158). Both features are included in the model feature set and are passed to all models as continuous numeric inputs. The value -1 carries no ordinal meaning in this context; it is a missing-data indicator that happens to fall below the minimum meaningful score of zero. These features were retained without re-encoding because altering them would create a mismatch with the saved production model artifact that the Streamlit dashboard depends on. Proper encoding — for example, replacing -1 with NaN followed by median imputation, or introducing a binary indicator variable — is listed in future work. The presence of sentinel values may introduce a systematic artefact into the learned feature space for tree-based models and a sign-reversal artefact for linear models.

### 3.9.2 Near-Constant Features After Median Imputation

Five features have missingness rates exceeding 88% of records: leftVision (94.3%), rightVision (92.4%), bloodMaxPressure (91.8%), bloodMinPressure (91.8%), and restingHeartRate (88.6%). After training-set median imputation, these five features take a single constant value for the majority of records in any given training fold, contributing negligible variance and therefore negligible predictive signal. SHAP analysis on the full production model confirms near-zero contribution from each of these features. They are retained for consistency with the production model artifact. Their presence inflates the nominal feature count without proportional contribution to predictive performance, and this should be borne in mind when interpreting the feature group ablation results in Experiment 3.

### 3.9.3 Redundant Derived Feature Within the Postural Risk Group

The feature aggregated_postural_index is defined as the arithmetic mean of six postural risk scores: frontHeadRisk, humpbackRisk, kneeRisk, pelvisRisk, postureRisk, and spineRisk. All six of these component features are themselves present as individual variables in the model feature set and belong to the same postural risk group used in Experiment 3. The aggregate therefore carries no independent information relative to its components when all six are simultaneously available, as is the case in all experiments. The feature was included in the original model training in Health_Pipeline.ipynb and is retained here for consistency. The redundancy does not affect the qualitative conclusions of the feature group ablation because the postural risk group as a whole (including the aggregate) is assessed against the other groups, but it does mean that the postural risk group nominally contains ten features while functionally contributing information from at most nine.

### 3.9.4 Statistical Power of the Wilcoxon Test Under Bonferroni Correction

All three experiments rely on the Wilcoxon signed-rank test for pairwise significance assessment, using 30 paired fold observations per comparison. The corrected significance thresholds are 0.005 (Experiment 1), 0.0167 (Experiment 2), and 0.0083 (Experiment 3). At 30 paired observations and a corrected alpha of 0.005, the test has limited power to detect moderate effect sizes in the range of Cohen's d = 0.3 to 0.5. The practical consequence is that a non-significant result cannot be interpreted as evidence that the compared models or feature sets perform equivalently on this task. It means only that, given the available data, the test is unable to distinguish their performance distributions with sufficient confidence under the applied multiple-comparison correction. The root cause is the dataset size: 53 unique individuals is insufficient for high-power pairwise testing after Bonferroni correction. This is a study limitation inherent to the data collection context and is not a methodological error.
