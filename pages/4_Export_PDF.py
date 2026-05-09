"""
Page 4 — Export PDF
Generates and downloads a one-page PDF report for the active client.
Requires an active scan from Individual Report or Upload New Scan.
"""

import numpy as np
import streamlit as st

from app_utils import generate_pdf_report, load_population

st.set_page_config(page_title="Export PDF — Zdravoletie", layout="wide")
st.title("Export PDF Report")

# ── Guard: require active scan ────────────────────────────────────────────────
if "active_gap" not in st.session_state:
    st.warning(
        "No active scan selected. "
        "Go to **Individual Report** or **Upload New Scan** first."
    )
    st.page_link("pages/1_Individual_Report.py", label="Go to Individual Report")
    st.page_link("pages/2_Upload_New_Scan.py", label="Go to Upload New Scan")
    st.stop()

client_gap   = st.session_state["active_gap"]
client_label = st.session_state["active_label"]
shap_vals    = st.session_state["active_shap"]
features     = st.session_state["active_features"]
source       = st.session_state.get("active_source", "unknown")

# ── Report preview ────────────────────────────────────────────────────────────
st.subheader("Report preview")

direction = "above" if client_gap >= 0 else "below"
col1, col2, col3 = st.columns(3)
col1.metric("Client",          client_label)
col2.metric("Age gap",         f"{client_gap:+.2f} y")
col3.metric("Source",          "Database" if source == "database" else "Uploaded scan")

st.markdown(
    f"The report will include:\n"
    f"- **Client summary**: age gap ({client_gap:+.2f} y, {abs(client_gap):.2f} y {direction} "
    f"chronological age) and population percentile\n"
    f"- **SHAP feature contribution chart**: top 12 features by absolute contribution\n"
    f"- **Population histogram**: client position in the 158-record age gap distribution"
)

st.markdown("---")

# ── Generate PDF ──────────────────────────────────────────────────────────────
df_pop   = load_population()
pop_gaps = df_pop["age_gap"].dropna().values

with st.spinner("Generating PDF..."):
    try:
        pdf_bytes = generate_pdf_report(
            client_label  = client_label,
            gap           = client_gap,
            shap_vals     = np.array(shap_vals),
            feature_names = features,
            population_gaps = pop_gaps,
        )
    except Exception as e:
        st.error(f"PDF generation failed: {e}")
        st.stop()

# ── Download button ───────────────────────────────────────────────────────────
safe_name = client_label.replace(" ", "_").replace("/", "-").replace(":", "")[:40]
filename  = f"zdravoletie_report_{safe_name}.pdf"

st.download_button(
    label="Download PDF report",
    data=pdf_bytes,
    file_name=filename,
    mime="application/pdf",
)

st.caption(
    "The PDF is generated client-side and is not stored on any server. "
    "It can be attached to client records or printed for clinical review."
)
