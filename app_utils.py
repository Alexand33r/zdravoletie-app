"""
Shared utilities for all Streamlit pages.
All model and data paths are relative to the repo root so the app
deploys to Streamlit Community Cloud without modification.
"""

from io import BytesIO
from datetime import date
from typing import Optional

import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import shap
import streamlit as st

from translations import TRANSLATIONS


# ── Asset loading (cached for the session lifetime) ───────────────────────────

@st.cache_resource
def load_assets():
    model  = joblib.load("models/anovator_age_gap_model.joblib")
    scaler = joblib.load("models/anovator_biological_scaler.joblib")
    with open("models/model_features.json") as f:
        features = json.load(f)
    try:
        with open("models/training_medians.json") as f:
            medians = json.load(f)
    except FileNotFoundError:
        # Fall back to population medians computed at runtime
        medians = {}
    return model, scaler, features, medians


@st.cache_data
def load_population() -> pd.DataFrame:
    return pd.read_csv("data/Anovator_Biological_Master.csv")


@st.cache_resource
def get_explainer(_model):
    return shap.TreeExplainer(_model)


@st.cache_data
def get_training_medians(features: tuple) -> dict:
    """Compute feature medians from the population CSV as fallback when
    training_medians.json is absent. Cached so it runs only once."""
    df = load_population()
    # Apply derived features before computing medians
    df = _add_derived_features(df)
    result = {}
    for feat in features:
        if feat in df.columns:
            val = df[feat].median()
            if pd.notna(val):
                result[feat] = float(val)
    return result


# ── Feature engineering ───────────────────────────────────────────────────────

DERIVED_FEATURES = {
    "sex_encoded", "muscle_fat_ratio",
    "upper_lower_muscle_ratio", "trunk_limb_fat_ratio",
    "aggregated_postural_index",
}

LIMB_FAT_COLS   = ["fatLeftArm", "fatRightArm", "fatLeftLeg", "fatRightLeg"]
POSTURAL_COLS   = ["humpbackRisk", "spineRisk", "pelvisRisk",
                   "postureRisk", "kneeRisk", "frontHeadRisk"]

# Minimum raw columns needed to derive the 5 engineered features
UPLOAD_REQUIRED_COLS = [
    "sex", "fat", "muscle", "upperBody", "lowerBody",
    "fatTrunk", *LIMB_FAT_COLS, *POSTURAL_COLS,
]


def _add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "sex" in df.columns and "sex_encoded" not in df.columns:
        df["sex_encoded"] = df["sex"].map({"F": 0, "M": 1})
    df["muscle_fat_ratio"]        = df["muscle"] / (df["fat"] + 0.1)
    df["upper_lower_muscle_ratio"]= df["upperBody"] / (df["lowerBody"] + 0.1)
    df["trunk_limb_fat_ratio"]    = df["fatTrunk"] / (df[LIMB_FAT_COLS].sum(axis=1) + 0.1)
    df["aggregated_postural_index"]= df[POSTURAL_COLS].mean(axis=1)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    return df


def preprocess_input(
    df_raw: pd.DataFrame,
    features: list,
    medians: dict,
) -> pd.DataFrame:
    df = _add_derived_features(df_raw)
    df = df.reindex(columns=features)
    df = df.fillna(medians).fillna(0)
    return df


# ── Prediction + explanation ──────────────────────────────────────────────────

def predict_and_explain(
    df_raw: pd.DataFrame,
    model,
    scaler,
    features: list,
    medians: dict,
    explainer,
):
    """Returns (gap: float, shap_vals_1d: ndarray, X_scaled_1d: ndarray)."""
    df_proc  = preprocess_input(df_raw, features, medians)
    X_scaled = scaler.transform(df_proc)
    gap      = float(model.predict(X_scaled)[0])
    sv       = explainer.shap_values(X_scaled)
    # TreeExplainer returns shape (n_samples, n_features) for regressors
    shap_vals = sv[0] if sv.ndim == 2 else sv
    return gap, shap_vals, X_scaled[0]


# ── Visualisation helpers ─────────────────────────────────────────────────────

FEATURE_LABELS = {
    # Body composition
    "fat":                      "Total fat mass (kg)",
    "muscle":                   "Total muscle mass (kg)",
    "upperBody":                "Upper body muscle (kg)",
    "lowerBody":                "Lower body muscle (kg)",
    "fatTrunk":                 "Trunk fat mass (kg)",
    "fatLeftArm":               "Left arm fat (kg)",
    "fatRightArm":              "Right arm fat (kg)",
    "fatLeftLeg":               "Left leg fat (kg)",
    "fatRightLeg":              "Right leg fat (kg)",
    "bmi":                      "BMI",
    "weight":                   "Body weight (kg)",
    "height":                   "Height (cm)",
    "wc":                       "Waist circumference (cm)",
    "bodyFat":                  "Body fat %",
    "trunkFat":                 "Trunk fat %",
    "muscleMass":               "Muscle mass",
    "visceralFat":              "Visceral fat level",
    "boneMass":                 "Bone mass (kg)",
    "metabolicAge":             "Metabolic age",
    # Bioimpedance — R20
    "r20LeftLeg":               "Left leg resistance R20 (Ω)",
    "r20RightLeg":              "Right leg resistance R20 (Ω)",
    "r20LeftArm":               "Left arm resistance R20 (Ω)",
    "r20RightArm":              "Right arm resistance R20 (Ω)",
    "r20Trunk":                 "Trunk resistance R20 (Ω)",
    # Bioimpedance — R100
    "r100LeftLeg":              "Left leg resistance R100 (Ω)",
    "r100RightLeg":             "Right leg resistance R100 (Ω)",
    "r100LeftArm":              "Left arm resistance R100 (Ω)",
    "r100RightArm":             "Right arm resistance R100 (Ω)",
    "r100Trunk":                "Trunk resistance R100 (Ω)",
    "phaseAngle":               "Bioimpedance phase angle (°)",
    # Postural risk scores
    "humpbackRisk":             "Humpback risk score",
    "spineRisk":                "Spine alignment risk",
    "pelvisRisk":               "Pelvis alignment risk",
    "postureRisk":              "Overall posture risk",
    "kneeRisk":                 "Knee alignment risk",
    "frontHeadRisk":            "Forward head posture risk",
    # Derived / engineered features
    "sex_encoded":              "Sex (F=0, M=1)",
    "muscle_fat_ratio":         "Muscle-to-fat ratio",
    "upper_lower_muscle_ratio": "Upper/lower muscle ratio",
    "trunk_limb_fat_ratio":     "Trunk-to-limb fat ratio",
    "aggregated_postural_index":"Composite postural risk",
    # Other numeric inputs
    "age":                      "Chronological age (years)",
    "aerobicGoal":              "Aerobic fitness goal",
    "sportSafeRisk":            "Sport safety risk",
    "sportLevel":               "Sport activity level",
    "leftVision":               "Left eye vision",
    "rightVision":              "Right eye vision",
    "bloodMaxPressure":         "Systolic blood pressure",
    "bloodMinPressure":         "Diastolic blood pressure",
    "restingHeartRate":         "Resting heart rate (bpm)",
}


def shap_bar_figure(
    shap_vals: np.ndarray,
    feature_names: list,
    max_features: int = 15,
    title: str = "Feature Contributions to Predicted Age Gap",
) -> plt.Figure:
    order  = np.argsort(np.abs(shap_vals))[-max_features:]
    vals   = shap_vals[order]
    names  = [FEATURE_LABELS.get(feature_names[i], feature_names[i]) for i in order]
    colors = ["#d62728" if v > 0 else "#1f77b4" for v in vals]

    fig, ax = plt.subplots(figsize=(9, max(4, max_features * 0.45)))
    ax.barh(range(len(vals)), vals, color=colors, alpha=0.85, edgecolor="white")
    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels(names, fontsize=9)
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel("SHAP value (years added to age gap)", fontsize=10)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.annotate(
        "Red = increases biological age gap   |   Blue = protective",
        xy=(0.5, -0.12), xycoords="axes fraction",
        ha="center", fontsize=8, color="gray",
    )
    plt.tight_layout()
    return fig


def population_hist_figure(
    population_gaps: np.ndarray,
    client_gap: float,
    client_label: str,
) -> plt.Figure:
    percentile = float(np.mean(population_gaps < client_gap) * 100)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(population_gaps, bins=25, color="#aec6e8", edgecolor="white", alpha=0.9, label="Population (n=158)")
    ax.axvline(
        client_gap, color="#d62728", linewidth=2.2, linestyle="--",
        label=f"{client_label}: {client_gap:+.2f} y  (P{percentile:.0f})",
    )
    ax.set_xlabel("Age gap = bodyAge − age (years)", fontsize=10)
    ax.set_ylabel("Number of records", fontsize=10)
    ax.set_title("Population Age Gap Distribution", fontsize=11, fontweight="bold")
    ax.legend(fontsize=9)
    plt.tight_layout()
    return fig


def population_scatter_figure(
    df_pop: pd.DataFrame,
    client_age: Optional[float],
    client_gap: float,
    client_label: str,
) -> plt.Figure:
    ages = df_pop["age"].dropna().values
    gaps = df_pop["age_gap"].dropna().values
    # Only use rows with both columns present
    mask = df_pop["age"].notna() & df_pop["age_gap"].notna()
    ages = df_pop.loc[mask, "age"].values
    gaps = df_pop.loc[mask, "age_gap"].values

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(ages, gaps, color="#aec6e8", alpha=0.7, s=40, edgecolors="white", linewidths=0.5, label="Population (n=158)")
    if client_age is not None:
        ax.scatter(
            [client_age], [client_gap],
            color="#d62728", s=90, zorder=5,
            label=f"{client_label}: age {client_age:.0f}, gap {client_gap:+.2f} y",
        )
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.set_xlabel("Chronological age (years)", fontsize=10)
    ax.set_ylabel("Age gap = bodyAge − age (years)", fontsize=10)
    ax.set_title("Age vs Age Gap — Population Scatter", fontsize=11, fontweight="bold")
    ax.legend(fontsize=9)
    plt.tight_layout()
    return fig


# ── PDF generation ────────────────────────────────────────────────────────────

def generate_pdf_report(
    client_label: str,
    gap: float,
    shap_vals: np.ndarray,
    feature_names: list,
    population_gaps: np.ndarray,
) -> bytes:
    """Returns PDF bytes for st.download_button."""
    percentile   = float(np.mean(population_gaps < gap) * 100)
    direction    = "above" if gap >= 0 else "below"
    gap_abs      = abs(gap)

    fig = plt.figure(figsize=(15, 10))
    gs  = gridspec.GridSpec(
        2, 2, figure=fig,
        height_ratios=[0.28, 1],
        hspace=0.45, wspace=0.38,
    )

    # ── Header panel ──────────────────────────────────────────────────────────
    ax_hdr = fig.add_subplot(gs[0, :])
    ax_hdr.axis("off")
    header = (
        f"ZDRAVOLETIE BIOMETRIC INTELLIGENCE REPORT\n"
        f"Client: {client_label}    |    Generated: {date.today().strftime('%d %B %Y')}\n\n"
        f"Predicted Age Gap:  {gap:+.2f} years  "
        f"({gap_abs:.2f} y {direction} chronological age)\n"
        f"Population percentile:  {percentile:.0f}th  "
        f"(higher = biologically older relative to the 158-record population)"
    )
    ax_hdr.text(
        0.02, 0.5, header,
        transform=ax_hdr.transAxes,
        fontsize=10.5, verticalalignment="center",
        fontfamily="monospace",
        bbox=dict(boxstyle="round,pad=0.6", facecolor="#eef2f7", alpha=0.9),
    )

    # ── SHAP bar chart ────────────────────────────────────────────────────────
    ax_shap = fig.add_subplot(gs[1, 0])
    max_f   = 12
    order   = np.argsort(np.abs(shap_vals))[-max_f:]
    vals    = shap_vals[order]
    names   = [feature_names[i] for i in order]
    colors  = ["#d62728" if v > 0 else "#1f77b4" for v in vals]
    ax_shap.barh(range(len(vals)), vals, color=colors, alpha=0.85, edgecolor="white")
    ax_shap.set_yticks(range(len(vals)))
    ax_shap.set_yticklabels(names, fontsize=8)
    ax_shap.axvline(0, color="black", linewidth=0.7, linestyle="--")
    ax_shap.set_xlabel("SHAP value (years)", fontsize=9)
    ax_shap.set_title(
        "Feature Contributions\nRed = ages faster  |  Blue = protective",
        fontsize=9, fontweight="bold",
    )

    # ── Population histogram ──────────────────────────────────────────────────
    ax_pop = fig.add_subplot(gs[1, 1])
    ax_pop.hist(population_gaps, bins=22, color="#aec6e8", edgecolor="white", alpha=0.9)
    ax_pop.axvline(gap, color="#d62728", linewidth=2, linestyle="--",
                   label=f"Client: {gap:+.2f} y (P{percentile:.0f})")
    ax_pop.set_xlabel("Age gap (years)", fontsize=9)
    ax_pop.set_ylabel("Records", fontsize=9)
    ax_pop.set_title("Population Distribution\n(158 Anovator records)", fontsize=9, fontweight="bold")
    ax_pop.legend(fontsize=8)

    buf = BytesIO()
    fig.savefig(buf, format="pdf", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


# ── Upload validation ─────────────────────────────────────────────────────────

def validate_upload(df: pd.DataFrame, features: list) -> tuple[bool, list, list]:
    """Returns (ok, missing_required, imputed_features).
    ok is False only if core derivation columns are absent.
    """
    missing_required = [c for c in UPLOAD_REQUIRED_COLS if c not in df.columns]
    derived = DERIVED_FEATURES
    raw_model_feats  = [f for f in features if f not in derived]
    imputed_features = [f for f in raw_model_feats if f not in df.columns]
    ok = len(missing_required) == 0
    return ok, missing_required, imputed_features


def make_template_csv(features: list) -> str:
    """Return a CSV string with one empty-valued header row for user guidance."""
    df = load_population()
    derived = DERIVED_FEATURES
    raw_cols = [c for c in df.columns if c not in derived and c != "age_gap"]
    template = pd.DataFrame(columns=raw_cols)
    return template.to_csv(index=False)


# ── UI helpers (language, sidebar) ────────────────────────────────────────────

_LOGO_SVG_SIDEBAR = """
<div style="text-align:center; padding: 8px 0 4px 0;">
  <svg width="44" height="44" viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg">
    <circle cx="22" cy="22" r="21" fill="#2E7D32"/>
    <text x="22" y="22" dominant-baseline="central" text-anchor="middle"
      font-family="sans-serif" font-size="24" font-weight="bold" fill="white">Z</text>
  </svg>
  <div style="font-weight:700; font-size:13px; color:#2E7D32; margin-top:3px; letter-spacing:0.5px;">
    Zdravoletie AI
  </div>
</div>
"""

_LOGO_SVG_LANDING = """
<div style="text-align:center; margin-bottom:12px;">
  <svg width="72" height="72" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">
    <circle cx="36" cy="36" r="34" fill="#2E7D32"/>
    <text x="36" y="36" dominant-baseline="central" text-anchor="middle"
      font-family="sans-serif" font-size="40" font-weight="bold" fill="white">Z</text>
  </svg>
</div>
"""


def get_text(key: str, lang: str) -> str:
    """Look up a translated string from TRANSLATIONS.
    Falls back to English if the key or language is missing.
    """
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    return entry.get(lang) or entry.get("en") or key


def render_sidebar_header() -> str:
    """Render the consistent sidebar header (logo, app name, language toggle).
    Must be called before any page-specific sidebar widgets.
    Returns the active language code: 'en' or 'bg'.
    """
    if "language" not in st.session_state:
        st.session_state["language"] = "en"

    st.sidebar.markdown(_LOGO_SVG_SIDEBAR, unsafe_allow_html=True)
    st.sidebar.markdown("---")

    lang = st.session_state["language"]
    idx = 0 if lang == "en" else 1
    choice = st.sidebar.selectbox(
        "English / Български",
        ["English", "Български"],
        index=idx,
        key="lang_select",
    )
    st.session_state["language"] = "en" if choice == "English" else "bg"
    return st.session_state["language"]


def render_sidebar_footer(lang: str) -> None:
    """Render the disclaimer at the bottom of the sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.caption(get_text("disclaimer", lang))


def landing_logo_html() -> str:
    """Return the large landing-page Z logo as an HTML string."""
    return _LOGO_SVG_LANDING


def gap_metric_html(label: str, value_str: str, value: float, invert: bool = False) -> str:
    """Return an HTML card for an age-gap metric.

    invert=True reverses color logic (positive value = green), used for
    'Potential gain' where a larger positive number means improvement.
    """
    if value > 0:
        color   = "#2E7D32" if invert else "#E65100"
        arrow   = "↑"
        sublabel = "Improvement" if invert else "Older than age"
    elif value < 0:
        color   = "#E65100" if invert else "#2E7D32"
        arrow   = "↓"
        sublabel = "Worsened" if invert else "Younger than age"
    else:
        color   = "#757575"
        arrow   = "—"
        sublabel = "No change"

    return (
        f'<div style="border-left:4px solid {color}; padding:10px 16px; '
        f'border-radius:4px; background:#f9f9f9; margin:4px 0;">'
        f'<div style="font-size:12px; color:#666; margin-bottom:4px;">{label}</div>'
        f'<div style="font-size:24px; font-weight:700; color:{color};">'
        f'{arrow} {value_str}</div>'
        f'<div style="font-size:11px; color:{color}; margin-top:2px;">{sublabel}</div>'
        f'</div>'
    )
