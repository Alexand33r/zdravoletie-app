"""
Central configuration for the Zdravoletie thesis project.

All stochastic operations must use RANDOM_SEED.
All file paths are relative to the repository root.
Import this module rather than hardcoding values anywhere.
"""

# ── Reproducibility ───────────────────────────────────────────────────────────
RANDOM_SEED = 42

# ── Data paths ────────────────────────────────────────────────────────────────
PATH_MASTER_CSV      = "data/Anovator_Biological_Master.csv"
PATH_SYNTHETIC_CSV   = "data/Anovator_Synthetic_Population_1000.csv"
PATH_CLEANED_CSV     = "data/Anovator_Final_Cleaned_Dataset.csv"

# ── Model artifact paths ──────────────────────────────────────────────────────
PATH_MODEL           = "models/anovator_age_gap_model.joblib"
PATH_SCALER          = "models/anovator_biological_scaler.joblib"
PATH_MODEL_FEATURES  = "models/model_features.json"
PATH_TRAINING_MEDIANS = "models/training_medians.json"

# ── Output directories ────────────────────────────────────────────────────────
DIR_RESULTS = "results"
DIR_MODELS  = "models"
DIR_DATA    = "data"
DIR_THESIS  = "thesis"

# ── Cross-validation protocol (all three experiments) ────────────────────────
# N_CV_SPLITS=30 is the standard choice for repeated GroupShuffleSplit.
# With 53 individuals and test_size=0.20, each split yields ~13 test rows,
# so fold-to-fold MAE variance is high. 30 splits gives stable mean estimates;
# increasing to 50 would narrow 95% CIs by ~18% but at 67% more runtime.
N_CV_SPLITS  = 30
TEST_SIZE    = 0.20  # fraction of unique individuals held out per split
GROUP_COLUMN = "name"

# ── Statistical testing ───────────────────────────────────────────────────────
CONFIDENCE_LEVEL = 0.95
ALPHA            = 0.05
# Bonferroni correction: 5 models -> C(5,2) = 10 unique pairs -> alpha/10
# Note: the Wilcoxon signed-rank test on n=30 pairs at alpha=0.005 has limited
# power to detect moderate effect sizes. Non-significant results must be
# reported as inconclusive, NOT as evidence of model equivalence.
N_MODEL_PAIRS    = 10
BONFERRONI_ALPHA = ALPHA / N_MODEL_PAIRS  # 0.005

# ── Model registry (Experiments 1 and 2) ─────────────────────────────────────
MODEL_NAMES = [
    "RandomForest",
    "Ridge",
    "SVR",
    "GradientBoosting",
    "HistGradientBoosting",
]

# Hyperparameters for each model — used identically in all three experiments.
# sklearn defaults are used except where noted.
# RandomForest: max_depth=7 overrides the unlimited default to prevent overfitting
#   on ~145 training rows; consistent with Health_Pipeline.ipynb.
# DO NOT import tuned params from Benchmarkinig.ipynb — those were optimised on
#   synthetic pseudo-labels and would bias the real-data comparison.
MODEL_HYPERPARAMS = {
    "RandomForest":        {"n_estimators": 100, "max_depth": 7, "random_state": RANDOM_SEED},
    "Ridge":               {"alpha": 1.0},
    "SVR":                 {"kernel": "rbf", "C": 1.0, "epsilon": 0.1},
    "GradientBoosting":    {"n_estimators": 100, "learning_rate": 0.1, "max_depth": 3,
                            "random_state": RANDOM_SEED},
    "HistGradientBoosting":{"max_iter": 100, "random_state": RANDOM_SEED},
}

# ── Feature groups for Experiment 3 ──────────────────────────────────────────
# Groups are ADDITIVE and CUMULATIVE:
#   Group 1 = ANTHROPOMETRIC_AND_METABOLIC          (63 features)
#   Group 2 = + BIOIMPEDANCE                        (73 features)
#   Group 3 = + POSTURAL_RISK                       (83 features)
#   Group 4 = + JOINT_ANGLES  (= all model features) (88 features)
#
# "Anthropometric and metabolic" is the correct label for the base group.
# It includes body composition, dimensions, Anovator-computed recommendations
# (aerobicGoal etc.), optional vital signs, fitness tests, and demographics.
# Calling it "body composition only" would be inaccurate and indefensible.
#
# Known issue: aggregated_postural_index (in POSTURAL_RISK) is a derived mean
# of 6 features also in that group. It adds no independent information within
# the group but is retained for consistency with the trained model artifact.
#
# Known issue: sportSafeRisk and sportLevel use -1 as a sentinel for "not
# computed" (37% and 70% of records respectively). These are in the base group
# and treated as numeric — a limitation noted in the thesis methodology.
#
# Known issue: 5 features have >88% missingness (rightVision, leftVision,
# bloodMaxPressure, bloodMinPressure, restingHeartRate). After median imputation
# they are near-constants and contribute negligible model signal. Retained for
# consistency with the trained model.
#
# At runtime, compute the base group as:
#   set(model_features) - BIOIMPEDANCE - POSTURAL_RISK - JOINT_ANGLES

FEATURES_BIOIMPEDANCE = [
    "r20LeftArm",   "r20RightArm",  "r20LeftLeg",  "r20RightLeg",  "r20Trunk",
    "r100LeftArm",  "r100RightArm", "r100LeftLeg", "r100RightLeg", "r100Trunk",
]

FEATURES_POSTURAL_RISK = [
    "frontHeadRisk", "headRisk",    "humpbackRisk", "kneeRisk",
    "pelvisRisk",    "postureRisk", "shoulderRisk", "spineRisk",
    "side_hunchback_risk", "aggregated_postural_index",
]

FEATURES_JOINT_ANGLES = [
    "front_shoulder_angle",
    "front_left_leg_angle",
    "front_right_leg_angle",
    "side_left_leg_angle",
    "side_right_leg_angle",
]

# BODY_COMPOSITION is derived at runtime:
#   model_features - BIOIMPEDANCE - POSTURAL_RISK - JOINT_ANGLES
FEATURES_ADDITIVE_GROUPS = [
    FEATURES_BIOIMPEDANCE,
    FEATURES_POSTURAL_RISK,
    FEATURES_JOINT_ANGLES,
]
