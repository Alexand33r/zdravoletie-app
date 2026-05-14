"""
Page 4 — Export PDF
Generates and downloads a one-page PDF report for the active client.
Requires an active scan from Individual Report or Upload New Scan.
"""

import numpy as np
import streamlit as st

from app_utils import (
    get_text,
    render_sidebar_header,
    render_sidebar_footer,
    generate_pdf_report,
    load_population,
)

st.set_page_config(page_title="Export PDF — Zdravoletie", layout="wide")

# ── Sidebar ───────────────────────────────────────────────────────────────────
lang = render_sidebar_header()
render_sidebar_footer(lang)

# ── Page header ───────────────────────────────────────────────────────────────
st.title(get_text("page_export_title", lang))

# ── Guard: require active scan ────────────────────────────────────────────────
if "active_gap" not in st.session_state:
    st.warning(get_text("warn_no_scan", lang))
    st.page_link("pages/1_Individual_Report.py", label=get_text("link_go_individual", lang))
    st.page_link("pages/2_Upload_New_Scan.py",   label=get_text("link_go_upload", lang))
    st.stop()

client_gap   = st.session_state["active_gap"]
client_label = st.session_state["active_label"]
shap_vals    = st.session_state["active_shap"]
features     = st.session_state["active_features"]
source       = st.session_state.get("active_source", "unknown")

# ── Report preview ────────────────────────────────────────────────────────────
st.subheader(get_text("section_report_preview", lang))

source_label = (
    get_text("source_database", lang) if source == "database"
    else get_text("source_uploaded", lang)
)

col1, col2, col3 = st.columns(3)
col1.metric(get_text("metric_client", lang),    client_label)
col2.metric(get_text("metric_age_gap", lang),   f"{client_gap:+.2f} y")
col3.metric(get_text("metric_source", lang),    source_label)

st.markdown(f"{get_text('report_will_include', lang)}")
st.markdown(f"- {get_text('report_item_summary', lang)}")
st.markdown(f"- {get_text('report_item_shap', lang)}")
st.markdown(f"- {get_text('report_item_hist', lang)}")

st.markdown("---")

# ── Generate PDF ──────────────────────────────────────────────────────────────
df_pop   = load_population()
pop_gaps = df_pop["age_gap"].dropna().values

with st.spinner(get_text("spinner_pdf", lang)):
    try:
        pdf_bytes = generate_pdf_report(
            client_label    = client_label,
            gap             = client_gap,
            shap_vals       = np.array(shap_vals),
            feature_names   = features,
            population_gaps = pop_gaps,
        )
    except Exception as e:
        st.error(get_text("err_pdf_failed", lang) + str(e))
        st.stop()

# ── Download button ───────────────────────────────────────────────────────────
safe_name = client_label.replace(" ", "_").replace("/", "-").replace(":", "")[:40]
filename  = f"zdravoletie_report_{safe_name}.pdf"

st.download_button(
    label=get_text("btn_download_pdf", lang),
    data=pdf_bytes,
    file_name=filename,
    mime="application/pdf",
)

st.caption(get_text("pdf_caption", lang))
