"""
Page 0 — About
Displayed first in the sidebar. Describes what the tool does, what it predicts,
and its known limitations.
"""

import streamlit as st

st.set_page_config(page_title="About — Zdravoletie", layout="wide")
st.title("About This Dashboard")
st.markdown("---")

st.markdown(
    """
    This dashboard is a research tool developed as part of a graduation thesis at
    Fontys University of Applied Sciences (BSc Applied Mathematics, Data Science).
    It provides a surrogate model and interpretability layer for the Anovator body
    scanning platform used at Zdravoletie, a health and rehabilitation centre in
    Varna, Bulgaria. The dashboard allows clinic staff to select an existing client
    scan, upload a new scan CSV, and view which biometric features drive the model's
    prediction — alongside a histogram showing where the client sits in the
    population of 158 recorded scans. A one-page PDF report can be downloaded for
    clinical records.
    """
)

st.markdown(
    """
    **What the model predicts.**
    The model predicts the Anovator *age gap*: the difference between the Anovator
    platform's proprietary bodyAge score and the client's chronological age. It does
    not predict clinical biological age in the medical sense — bodyAge is a
    commercial composite score whose formula is undisclosed and which has not been
    validated against mortality or morbidity endpoints. A predicted age gap of +3
    years means the surrogate model estimates that the Anovator formula would return
    a bodyAge three years above the client's chronological age, given the biometric
    inputs provided. It does not mean the client is clinically three years older than
    their chronological age. SHAP values shown in the dashboard reflect the model's
    learned approximation of the Anovator formula, not independently established
    physiological relationships.
    """
)

st.markdown(
    """
    **Known limitations.**
    The surrogate model was trained on 158 scan records from 53 unique individuals
    at a single clinic. Mean absolute error on held-out data is approximately 2.4
    years across 30 cross-validation folds, meaning individual predictions carry
    substantial uncertainty. Two features in the model — sportSafeRisk and
    sportLevel — use the value -1 as a sentinel for "not computed" and are treated
    as numeric inputs; this is a known encoding artefact. Five features
    (leftVision, rightVision, bloodMaxPressure, bloodMinPressure, restingHeartRate)
    are missing in more than 88% of records and contribute negligible signal after
    imputation. The model should not be used as a diagnostic instrument or as a
    substitute for clinical assessment. It is a research prototype intended to
    support interpretation of Anovator outputs, not to replace them.
    """
)

st.markdown("---")
st.caption(
    "Source code and experiment results: graduation thesis repository, Fontys University of Applied Sciences, 2026. "
    "Model trained on data from Zdravoletie, Varna, Bulgaria."
)
