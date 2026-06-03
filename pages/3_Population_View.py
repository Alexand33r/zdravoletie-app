"""
Page 3 — Population View
Histogram of age_gap across all 158 training records with the active client marked.
Requires an active scan from Individual Report or Upload New Scan.
"""

import numpy as np
import pandas as pd
import streamlit as st

from app_utils import (
    get_text,
    render_sidebar_header,
    render_sidebar_footer,
    load_population,
    population_hist_figure,
    population_scatter_figure,
    gap_metric_html,
)

st.set_page_config(page_title="Population View — Zdravoletie", layout="wide")

# ── Sidebar ───────────────────────────────────────────────────────────────────
lang = render_sidebar_header()
render_sidebar_footer(lang)

# ── Page header ───────────────────────────────────────────────────────────────
st.title(get_text("page_population_title", lang))

# ── Guard: require active scan ────────────────────────────────────────────────
if "active_gap" not in st.session_state:
    st.warning(get_text("warn_no_scan", lang))
    st.page_link("pages/1_Individual_Report.py", label=get_text("link_go_individual", lang))
    st.page_link("pages/2_Upload_New_Scan.py",   label=get_text("link_go_upload", lang))
    st.stop()

client_gap   = st.session_state["active_gap"]
client_label = st.session_state["active_label"]
client_age   = st.session_state.get("active_age", None)

# ── Load population ───────────────────────────────────────────────────────────
df_pop   = load_population()
pop_gaps = df_pop["age_gap"].dropna().values

percentile = float(np.mean(pop_gaps < client_gap) * 100)

# ── Summary metrics ───────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
if " (" in client_label:
    client_name, client_date = client_label.rsplit(" (", 1)
    client_date = client_date.rstrip(")")
else:
    client_name, client_date = client_label, ""
col1.markdown(
    f'<div style="border-left:4px solid #757575; padding:10px 16px; '
    f'border-radius:4px; background:#f9f9f9; margin:4px 0;">'
    f'<div style="font-size:12px; color:#666; margin-bottom:4px;">'
    f'{get_text("metric_client", lang)}</div>'
    f'<div style="font-size:16px; font-weight:700; color:#212121; word-break:break-word;">'
    f'{client_name}</div>'
    + (f'<div style="font-size:12px; color:#666; margin-top:2px;">{client_date}</div>'
       if client_date else "")
    + "</div>",
    unsafe_allow_html=True,
)
col2.markdown(
    gap_metric_html(get_text("metric_predicted_gap", lang), f"{client_gap:+.2f} y", client_gap),
    unsafe_allow_html=True,
)
col3.metric(get_text("metric_pop_pct", lang), f"{percentile:.0f}th")
pop_median = float(np.median(pop_gaps))
col4.markdown(
    gap_metric_html(get_text("metric_pop_median", lang), f"{pop_median:+.2f} y", pop_median),
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Histogram ─────────────────────────────────────────────────────────────────
fig = population_hist_figure(pop_gaps, client_gap, client_label)
st.pyplot(fig)

st.caption(get_text("hist_caption", lang))

st.markdown("---")

# ── Scatter plot: age vs age_gap ──────────────────────────────────────────────
st.subheader(get_text("section_scatter", lang))

fig_scatter = population_scatter_figure(df_pop, client_age, client_gap, client_label)
st.pyplot(fig_scatter)

scatter_caption_key = "scatter_caption_with_client" if client_age is not None else "scatter_caption_no_client"
st.caption(get_text(scatter_caption_key, lang))

st.markdown("---")

# ── Detailed population statistics ────────────────────────────────────────────
with st.expander(get_text("expander_pop_stats", lang)):
    stats = {
        get_text("stat_count",      lang): len(pop_gaps),
        get_text("stat_mean",       lang): f"{pop_gaps.mean():.2f} y",
        get_text("stat_std",        lang): f"{pop_gaps.std():.2f} y",
        get_text("stat_min",        lang): f"{pop_gaps.min():.2f} y",
        get_text("stat_p25",        lang): f"{np.percentile(pop_gaps, 25):.2f} y",
        get_text("stat_median",     lang): f"{np.median(pop_gaps):.2f} y",
        get_text("stat_p75",        lang): f"{np.percentile(pop_gaps, 75):.2f} y",
        get_text("stat_max",        lang): f"{pop_gaps.max():.2f} y",
        get_text("stat_client_gap", lang): f"{client_gap:+.2f} y",
        get_text("stat_client_pct", lang): f"{percentile:.0f}th",
    }
    st.table(
        pd.DataFrame.from_dict(
            stats, orient="index",
            columns=[get_text("stat_value", lang)],
        )
    )
