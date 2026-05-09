"""
Zdravoletie Biometric Intelligence Dashboard
Home / landing page.
"""

import streamlit as st

st.set_page_config(
    page_title="Zdravoletie AI",
    page_icon="",
    layout="wide",
)

st.title("Zdravoletie Biometric Intelligence")
st.markdown("---")

st.markdown(
    """
    This dashboard reverse-engineers the **Anovator bodyAge score** from raw biometric scan inputs
    and provides interpretable analysis of the factors driving each client's biological age gap.

    **Age gap** is defined as *bodyAge minus chronological age*. A positive value means the Anovator
    system judges the client as biologically older than their chronological age; negative means younger.
    """
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("1 — Individual Report")
    st.write(
        "Select an existing client from the 158-record population database. "
        "Run intervention simulations and view SHAP feature attributions."
    )
    st.page_link("pages/1_Individual_Report.py", label="Open Individual Report")

with col2:
    st.subheader("2 — Upload New Scan")
    st.write(
        "Upload a CSV export from an Anovator scan session to analyse a new client "
        "not in the training database."
    )
    st.page_link("pages/2_Upload_New_Scan.py", label="Open Upload")

with col3:
    st.subheader("3 — Population View")
    st.write(
        "See where the currently selected or uploaded client sits on the age gap "
        "distribution of all 158 training records."
    )
    st.page_link("pages/3_Population_View.py", label="Open Population View")

with col4:
    st.subheader("4 — Export PDF")
    st.write(
        "Download a one-page PDF report containing the age gap result, "
        "SHAP feature chart, and population histogram."
    )
    st.page_link("pages/4_Export_PDF.py", label="Open PDF Export")

st.markdown("---")
st.info(
    "Start with **Individual Report** to select an existing client, "
    "or **Upload New Scan** to analyse a new one. "
    "Population View and PDF Export require an active client selection."
)
