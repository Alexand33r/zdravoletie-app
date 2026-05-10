"""
Page 2 — Upload New Scan  (Priority 1 feature)
Upload a CSV with the same column structure as the Anovator training data.
Validates the file, runs prediction, stores results in session_state.
"""

import io

import numpy as np
import pandas as pd
import streamlit as st

from app_utils import (
    load_assets,
    load_population,
    get_explainer,
    get_training_medians,
    predict_and_explain,
    validate_upload,
    make_template_csv,
    shap_bar_figure,
    UPLOAD_REQUIRED_COLS,
)

st.set_page_config(page_title="Upload New Scan — Zdravoletie", layout="wide")
st.title("Upload New Scan")
st.markdown(
    "Upload a CSV export from an Anovator scan session. "
    "The file must contain the raw biometric columns — derived features and age gap "
    "are computed automatically."
)

# ── Load assets ───────────────────────────────────────────────────────────────
model, scaler, features, stored_medians = load_assets()
explainer = get_explainer(model)
medians   = stored_medians if stored_medians else get_training_medians(tuple(features))

# ── Template download ─────────────────────────────────────────────────────────
st.subheader("Step 1 — Download the column template")
template_csv = make_template_csv(features)
st.download_button(
    label="Download CSV template",
    data=template_csv,
    file_name="anovator_scan_template.csv",
    mime="text/csv",
    help="Open in Excel or a text editor, fill in your scan values, then upload below.",
)
st.caption(
    "The template contains all expected column headers. "
    "Fill in one row per scan. Columns left blank are imputed with training-set medians."
)

st.markdown("---")

# ── File upload ───────────────────────────────────────────────────────────────
st.subheader("Step 2 — Upload your completed CSV")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    help="Must be a UTF-8 CSV with Anovator biometric columns.",
)

if uploaded_file is None:
    st.info("No file uploaded yet.")
    st.stop()

# ── Parse ─────────────────────────────────────────────────────────────────────
try:
    df_upload = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Could not parse the file as CSV: {e}")
    st.stop()

if df_upload.empty:
    st.error("The uploaded file contains no data rows.")
    st.stop()

st.success(f"File loaded: {len(df_upload)} row(s), {len(df_upload.columns)} columns.")

# ── Validate ──────────────────────────────────────────────────────────────────
ok, missing_required, imputed_feats = validate_upload(df_upload, features)

if not ok:
    st.error(
        f"The file is missing {len(missing_required)} required column(s) that cannot be imputed:\n\n"
        + "\n".join(f"- `{c}`" for c in missing_required)
        + "\n\nDownload the template above, add these columns, and re-upload."
    )
    st.stop()

if imputed_feats:
    with st.expander(f"{len(imputed_feats)} column(s) not found — will be imputed with training medians"):
        st.write(imputed_feats)

# ── Row selection (if multiple rows uploaded) ──────────────────────────────────
if len(df_upload) > 1:
    st.subheader("Step 3 — Select which scan to analyse")

    # Try to show a useful label column
    label_col = next(
        (c for c in ("name", "date_created", "id") if c in df_upload.columns),
        None,
    )
    if label_col:
        row_labels = [
            f"Row {i + 1} — {df_upload.iloc[i][label_col]}"
            for i in range(len(df_upload))
        ]
    else:
        row_labels = [f"Row {i + 1}" for i in range(len(df_upload))]

    chosen_label = st.selectbox("Scan row", row_labels)
    chosen_idx   = row_labels.index(chosen_label)
else:
    chosen_idx   = 0
    chosen_label = "Row 1"

scan_row = df_upload.iloc[[chosen_idx]]

# ── Client label ──────────────────────────────────────────────────────────────
if "name" in scan_row.columns:
    client_name = str(scan_row["name"].iloc[0])
elif "id" in scan_row.columns:
    client_name = f"ID {scan_row['id'].iloc[0]}"
else:
    client_name = f"Uploaded client ({chosen_label})"

st.markdown("---")
st.subheader("Step 4 — Results")

# ── Predict ───────────────────────────────────────────────────────────────────
with st.spinner("Running prediction..."):
    try:
        gap, shap_vals, X_scaled = predict_and_explain(
            scan_row, model, scaler, features, medians, explainer
        )
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.stop()

# ── Store in session_state ────────────────────────────────────────────────────
st.session_state["active_gap"]      = gap
st.session_state["active_shap"]     = shap_vals
st.session_state["active_features"] = features
st.session_state["active_label"]    = client_name
st.session_state["active_source"]   = "upload"
if "age" in scan_row.columns and pd.notna(scan_row["age"].iloc[0]):
    st.session_state["active_age"] = float(scan_row["age"].iloc[0])
elif "active_age" in st.session_state:
    del st.session_state["active_age"]

# ── Display results ───────────────────────────────────────────────────────────
direction = "above" if gap >= 0 else "below"

col1, col2 = st.columns(2)
col1.metric("Predicted age gap", f"{gap:+.2f} years")
col2.metric(
    "Interpretation",
    f"{abs(gap):.2f} y {direction} chronological age",
)

st.markdown("---")

# ── SHAP bar chart ────────────────────────────────────────────────────────────
st.subheader("Feature Contributions")
fig = shap_bar_figure(shap_vals, features, title=f"Feature Contributions — {client_name}")
st.pyplot(fig)

st.caption(
    "Red features push the predicted age gap upward (biological ageing accelerators). "
    "Blue features push it downward (protective factors). Values are in years."
)

# ── Top risk and protective factors ──────────────────────────────────────────
pos_idx = np.argsort(shap_vals)[::-1]
neg_idx = np.argsort(shap_vals)

top_risk       = [(features[i], shap_vals[i]) for i in pos_idx if shap_vals[i] > 0][:5]
top_protective = [(features[i], shap_vals[i]) for i in neg_idx if shap_vals[i] < 0][:5]

col_r, col_p = st.columns(2)

with col_r:
    st.subheader("Top ageing accelerators")
    if top_risk:
        for feat, val in top_risk:
            st.write(f"**{feat}**: +{val:.3f} y")
    else:
        st.write("No features increasing the age gap.")

with col_p:
    st.subheader("Top protective factors")
    if top_protective:
        for feat, val in top_protective:
            st.write(f"**{feat}**: {val:.3f} y")
    else:
        st.write("No features reducing the age gap.")

st.markdown("---")
st.info(
    "Results stored. Navigate to **Population View** to see where this client sits "
    "in the full distribution, or **Export PDF** to download a report."
)
