"""
Page 1 — Individual Report
Select an existing client, run simulations, view SHAP feature attributions.
"""

import numpy as np
import pandas as pd
import streamlit as st

from app_utils import (
    load_assets,
    load_population,
    get_explainer,
    get_training_medians,
    predict_and_explain,
    preprocess_input,
    shap_bar_figure,
)

st.set_page_config(page_title="Individual Report — Zdravoletie", layout="wide")
st.title("Individual Report")
st.markdown("Select a client from the population database. Use the sliders to simulate interventions.")

# ── Load assets ───────────────────────────────────────────────────────────────
model, scaler, features, stored_medians = load_assets()
explainer = get_explainer(model)
df_pop    = load_population()

medians = stored_medians if stored_medians else get_training_medians(tuple(features))

# ── Client selection ──────────────────────────────────────────────────────────
st.sidebar.header("Client Selection")

unique_names = sorted(df_pop["name"].unique())
selected_name = st.sidebar.selectbox("Client name", unique_names)

client_records = df_pop[df_pop["name"] == selected_name].reset_index(drop=True)

if len(client_records) > 1:
    scan_labels = [
        f"Scan {i + 1} — {row['date_created'][:10]}"
        for i, row in client_records.iterrows()
    ]
    scan_choice = st.sidebar.selectbox("Scan date", scan_labels)
    scan_idx    = scan_labels.index(scan_choice)
else:
    scan_idx = 0

client_scan = client_records.iloc[[scan_idx]]

# ── Baseline prediction ───────────────────────────────────────────────────────
try:
    base_gap, base_shap, base_X = predict_and_explain(
        client_scan, model, scaler, features, medians, explainer
    )
except Exception as e:
    st.error(f"Prediction failed: {e}")
    st.stop()

# ── Simulation sliders ────────────────────────────────────────────────────────
st.sidebar.header("Simulate Intervention")
fat_red  = st.sidebar.slider("Target fat loss (kg)",    0.0, 10.0, 0.0, step=0.1)
mus_gain = st.sidebar.slider("Target muscle gain (kg)", 0.0,  5.0, 0.0, step=0.1)
wc_imp   = st.sidebar.slider("Waist circumference reduction (cm)", 0.0, 15.0, 0.0, step=0.5)

sim_scan = client_scan.copy()

fat_orig   = float(sim_scan["fat"].iloc[0])
fat_new    = max(1.0, fat_orig - fat_red)
actual_red = fat_orig - fat_new

if actual_red > 0 and fat_orig > 0:
    scale = fat_new / fat_orig
    for seg in ["fatLeftArm", "fatRightArm", "fatLeftLeg", "fatRightLeg", "fatTrunk"]:
        if seg in sim_scan.columns:
            sim_scan[seg] = sim_scan[seg] * scale

sim_scan["fat"]    = fat_new
sim_scan["weight"] = sim_scan["weight"] - actual_red
sim_scan["bmi"]    = sim_scan["weight"] / (sim_scan["height"] / 100) ** 2
sim_scan["muscle"] = sim_scan["muscle"] + mus_gain
sim_scan["wc"]     = sim_scan["wc"] - wc_imp

try:
    sim_gap, sim_shap, sim_X = predict_and_explain(
        sim_scan, model, scaler, features, medians, explainer
    )
except Exception as e:
    st.error(f"Simulation prediction failed: {e}")
    st.stop()

# ── Store active client in session_state for other pages ─────────────────────
st.session_state["active_gap"]      = sim_gap
st.session_state["active_shap"]     = sim_shap
st.session_state["active_features"] = features
st.session_state["active_label"]    = (
    f"{selected_name} ({client_records.iloc[scan_idx]['date_created'][:10]})"
)
st.session_state["active_source"]   = "database"
if "age" in client_scan.columns:
    st.session_state["active_age"] = float(client_scan["age"].iloc[0])

# ── Metrics ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Baseline age gap",  f"{base_gap:+.2f} y")
col2.metric(
    "Simulated age gap", f"{sim_gap:+.2f} y",
    delta=f"{sim_gap - base_gap:.2f}",
    delta_color="inverse",
)
col3.metric("Potential gain", f"{base_gap - sim_gap:.2f} y")

st.markdown("---")

# ── SHAP bar chart ────────────────────────────────────────────────────────────
st.subheader("Feature Contributions (Simulated Scan)")
fig = shap_bar_figure(sim_shap, features)
st.pyplot(fig)

st.caption(
    "SHAP values quantify each feature's contribution to the predicted age gap. "
    "Red features increase the predicted gap; blue features reduce it. "
    "Values are in years."
)

# ── Raw scan data (expandable) ────────────────────────────────────────────────
with st.expander("Raw scan values"):
    display_cols = [
        c for c in client_scan.columns
        if c not in ("id", "original_url", "bodyImage", "bodyImgOriginal", "bodyDetect")
    ]
    st.dataframe(client_scan[display_cols].T.rename(columns={client_scan.index[0]: "value"}))
