"""
Zdravoletie Biometric Intelligence Dashboard
Home / landing page.
"""

import streamlit as st

from app_utils import get_text, render_sidebar_header, render_sidebar_footer, landing_logo_html

st.set_page_config(
    page_title="Zdravoletie AI",
    page_icon="",
    layout="wide",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
lang = render_sidebar_header()
render_sidebar_footer(lang)

# ── Hero section ──────────────────────────────────────────────────────────────
st.markdown(landing_logo_html(), unsafe_allow_html=True)

st.markdown(
    f"<h1 style='text-align:center; color:#2E7D32; margin-top:0;'>{get_text('home_heading', lang)}</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style='text-align:center; font-size:16px; color:#424242; max-width:680px; margin:0 auto 8px auto;'>"
    f"{get_text('home_tagline', lang)}</p>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<p style='text-align:center; font-size:13px; color:#757575; max-width:640px; margin:0 auto 28px auto;'>"
    f"{get_text('age_gap_note', lang)}</p>",
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Navigation cards ──────────────────────────────────────────────────────────
_CARD_STYLE = (
    "background:#F5F5F5; border-radius:12px; padding:20px 22px 16px 22px; "
    "border:1px solid #E0E0E0; border-top:4px solid #2E7D32; "
    "min-height:150px;"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"<div style='{_CARD_STYLE}'>"
        f"<div style='font-size:17px; font-weight:700; color:#2E7D32; margin-bottom:8px;'>"
        f"1 — {get_text('nav_individual_title', lang)}</div>"
        f"<div style='font-size:13px; color:#424242; line-height:1.55;'>"
        f"{get_text('nav_individual_desc', lang)}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.page_link("pages/1_Individual_Report.py", label=get_text("nav_individual_btn", lang))

with col2:
    st.markdown(
        f"<div style='{_CARD_STYLE}'>"
        f"<div style='font-size:17px; font-weight:700; color:#2E7D32; margin-bottom:8px;'>"
        f"2 — {get_text('nav_upload_title', lang)}</div>"
        f"<div style='font-size:13px; color:#424242; line-height:1.55;'>"
        f"{get_text('nav_upload_desc', lang)}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.page_link("pages/2_Upload_New_Scan.py", label=get_text("nav_upload_btn", lang))

with col3:
    st.markdown(
        f"<div style='{_CARD_STYLE}'>"
        f"<div style='font-size:17px; font-weight:700; color:#2E7D32; margin-bottom:8px;'>"
        f"3 — {get_text('nav_population_title', lang)}</div>"
        f"<div style='font-size:13px; color:#424242; line-height:1.55;'>"
        f"{get_text('nav_population_desc', lang)}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.page_link("pages/3_Population_View.py", label=get_text("nav_population_btn", lang))

with col4:
    st.markdown(
        f"<div style='{_CARD_STYLE}'>"
        f"<div style='font-size:17px; font-weight:700; color:#2E7D32; margin-bottom:8px;'>"
        f"4 — {get_text('nav_export_title', lang)}</div>"
        f"<div style='font-size:13px; color:#424242; line-height:1.55;'>"
        f"{get_text('nav_export_desc', lang)}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.page_link("pages/4_Export_PDF.py", label=get_text("nav_export_btn", lang))

st.markdown("---")
st.info(get_text("home_tip", lang))

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    f"<div style='text-align:center; color:#9E9E9E; font-size:12px; margin-top:24px;'>"
    f"{get_text('footer', lang)}</div>",
    unsafe_allow_html=True,
)
