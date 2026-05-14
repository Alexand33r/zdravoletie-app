"""
Page 0 — About
Describes what the tool does, what it predicts, and its known limitations.
Bilingual: English / Bulgarian.
"""

import streamlit as st

from app_utils import get_text, render_sidebar_header, render_sidebar_footer

st.set_page_config(page_title="About — Zdravoletie", layout="wide")

# ── Sidebar ───────────────────────────────────────────────────────────────────
lang = render_sidebar_header()
render_sidebar_footer(lang)

# ── Content ───────────────────────────────────────────────────────────────────
st.title(get_text("page_about_title", lang))
st.markdown("---")

st.markdown(get_text("about_intro", lang))

st.markdown(f"**{get_text('about_what_predicts_title', lang)}**")
st.markdown(get_text("about_what_predicts_body", lang))

st.markdown(f"**{get_text('about_limitations_title', lang)}**")
st.markdown(get_text("about_limitations_body", lang))

st.markdown("---")
st.caption(get_text("about_caption", lang))
