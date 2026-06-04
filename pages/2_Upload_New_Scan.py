"""
Page 2 — Upload New Scan
Upload a CSV with the same column structure as the Anovator training data.
Validates the file, runs prediction, stores results in session_state.
"""

import io

import numpy as np
import pandas as pd
import streamlit as st

from app_utils import (
    get_text,
    render_sidebar_header,
    render_sidebar_footer,
    load_assets,
    load_population,
    get_explainer,
    get_training_medians,
    predict_and_explain,
    validate_upload,
    make_template_csv,
    shap_bar_figure,
    gap_metric_html,
    FEATURE_LABELS,
    UPLOAD_REQUIRED_COLS,
)

st.set_page_config(page_title="Upload New Scan — Zdravoletie", layout="wide")

# ── Sidebar ───────────────────────────────────────────────────────────────────
lang = render_sidebar_header()
render_sidebar_footer(lang)

# ── Page header ───────────────────────────────────────────────────────────────
st.title(get_text("page_upload_title", lang))
st.markdown(get_text("page_upload_desc", lang))

# ── Load assets ───────────────────────────────────────────────────────────────
model, scaler, features, stored_medians = load_assets()
explainer = get_explainer(model)
medians   = stored_medians if stored_medians else get_training_medians(tuple(features))

# ── Template download ─────────────────────────────────────────────────────────
st.subheader(get_text("step1_header", lang))
template_csv = make_template_csv(features)
st.download_button(
    label=get_text("btn_download_template", lang),
    data=template_csv,
    file_name="anovator_scan_template.csv",
    mime="text/csv",
    help=get_text("upload_help", lang),
)
st.caption(get_text("template_caption", lang))

st.markdown("---")

# ── File upload ───────────────────────────────────────────────────────────────
st.subheader(get_text("step2_header", lang))

uploaded_file = st.file_uploader(
    get_text("upload_label", lang),
    type=["csv"],
    help=get_text("upload_help", lang),
)

if uploaded_file is None:
    st.info(get_text("no_file_info", lang))
    st.stop()

# ── Parse ─────────────────────────────────────────────────────────────────────
try:
    df_upload = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(get_text("err_parse_csv", lang) + str(e))
    st.stop()

if df_upload.empty:
    st.error(get_text("err_empty_file", lang))
    st.stop()

st.success(
    get_text("file_loaded", lang).format(rows=len(df_upload), cols=len(df_upload.columns))
)

# ── Validate ──────────────────────────────────────────────────────────────────
ok, missing_required, imputed_feats = validate_upload(df_upload, features)

if not ok:
    st.error(
        f"**{get_text('err_missing_cols_title', lang)}**\n\n"
        + get_text("err_missing_cols_body", lang).format(n=len(missing_required))
    )
    st.markdown(f"**{get_text('err_missing_cols_listed', lang)}**")
    for col in missing_required:
        st.code(col)
    st.stop()

if imputed_feats:
    with st.expander(get_text("imputed_expander", lang).format(n=len(imputed_feats))):
        st.write(imputed_feats)

# ── Row selection (if multiple rows uploaded) ──────────────────────────────────
if len(df_upload) > 1:
    st.subheader(get_text("step3_header", lang))

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

    chosen_label = st.selectbox(get_text("lbl_scan_row", lang), row_labels)
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
st.subheader(get_text("step4_header", lang))

# ── Predict ───────────────────────────────────────────────────────────────────
with st.spinner(get_text("spinner_prediction", lang)):
    try:
        gap, shap_vals, X_scaled = predict_and_explain(
            scan_row, model, scaler, features, medians, explainer
        )
    except Exception as e:
        st.error(get_text("err_prediction_failed", lang) + str(e))
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
direction_key = "direction_above" if gap >= 0 else "direction_below"
direction_str = get_text(direction_key, lang)
interp = get_text("interpretation_fmt", lang).format(val=abs(gap), direction=direction_str)

col1, col2 = st.columns(2)
col1.markdown(
    gap_metric_html(get_text("metric_predicted_gap", lang), f"{gap:+.2f} y", gap),
    unsafe_allow_html=True,
)
col2.metric(get_text("metric_interpretation", lang), interp)

st.markdown("---")

# ── SHAP bar chart ────────────────────────────────────────────────────────────
st.subheader(get_text("section_feature_contributions_upload", lang))

with st.spinner(get_text("spinner_computing", lang)):
    fig = shap_bar_figure(
        shap_vals, features,
        title=f"{get_text('section_feature_contributions_upload', lang)} — {client_name}",
    )
st.pyplot(fig)

st.caption(get_text("shap_caption_upload", lang))

# ── Top risk and protective factors ──────────────────────────────────────────
pos_idx = np.argsort(shap_vals)[::-1]
neg_idx = np.argsort(shap_vals)

top_risk       = [(features[i], shap_vals[i]) for i in pos_idx if shap_vals[i] > 0][:5]
top_protective = [(features[i], shap_vals[i]) for i in neg_idx if shap_vals[i] < 0][:5]

col_r, col_p = st.columns(2)

with col_r:
    st.subheader(get_text("section_top_risk", lang))
    if top_risk:
        for feat, val in top_risk:
            label = FEATURE_LABELS.get(feat, feat)
            st.write(f"**{label}**: +{val:.3f} y")
    else:
        st.write(get_text("no_risk_features", lang))

with col_p:
    st.subheader(get_text("section_top_protective", lang))
    if top_protective:
        for feat, val in top_protective:
            label = FEATURE_LABELS.get(feat, feat)
            st.write(f"**{label}**: {val:.3f} y")
    else:
        st.write(get_text("no_protective_features", lang))

st.markdown("---")
st.info(get_text("nav_tip_upload", lang))
