"""
Page 3 — Population View
Histogram of age_gap across all 158 training records with the active client marked.
Requires an active scan from Individual Report or Upload New Scan.
"""

import numpy as np
import streamlit as st

from app_utils import load_population, population_hist_figure, population_scatter_figure

st.set_page_config(page_title="Population View — Zdravoletie", layout="wide")
st.title("Population View")

# ── Guard: require active scan ────────────────────────────────────────────────
if "active_gap" not in st.session_state:
    st.warning(
        "No active scan selected. "
        "Go to **Individual Report** to select a client from the database, "
        "or **Upload New Scan** to analyse a new scan."
    )
    st.page_link("pages/1_Individual_Report.py", label="Go to Individual Report")
    st.page_link("pages/2_Upload_New_Scan.py", label="Go to Upload New Scan")
    st.stop()

client_gap   = st.session_state["active_gap"]
client_label = st.session_state["active_label"]
client_age   = st.session_state.get("active_age", None)

# ── Load population ───────────────────────────────────────────────────────────
df_pop = load_population()
pop_gaps = df_pop["age_gap"].dropna().values

percentile = float(np.mean(pop_gaps < client_gap) * 100)

# ── Summary metrics ───────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Client", client_label)
col2.metric("Predicted age gap", f"{client_gap:+.2f} y")
col3.metric("Population percentile", f"{percentile:.0f}th")
col4.metric(
    "Population median",
    f"{np.median(pop_gaps):+.2f} y",
    help="Median age gap across all 158 Anovator records.",
)

st.markdown("---")

# ── Histogram ─────────────────────────────────────────────────────────────────
fig = population_hist_figure(pop_gaps, client_gap, client_label)
st.pyplot(fig)

st.caption(
    "The histogram shows the real age_gap distribution of the 158 Anovator scan records "
    "used for model training. The dashed red line marks the current client's predicted age gap. "
    "The population percentile indicates what fraction of the 158 records have a lower age gap."
)

st.markdown("---")

# ── Scatter plot: age vs age_gap ──────────────────────────────────────────────
st.subheader("Chronological Age vs Age Gap")

fig_scatter = population_scatter_figure(df_pop, client_age, client_gap, client_label)
st.pyplot(fig_scatter)

st.caption(
    "Each point represents one of the 158 Anovator scan records. "
    "The horizontal dashed line at zero marks no difference between bodyAge and chronological age. "
    "Points above the line have a bodyAge higher than their chronological age; points below are the reverse. "
    + ("The red point marks the current client." if client_age is not None
       else "Client age is not available for uploaded scans; the population points are shown without a client marker.")
)

st.markdown("---")

# ── Detailed population statistics ────────────────────────────────────────────
with st.expander("Population summary statistics"):
    import pandas as pd
    stats = {
        "Count":     len(pop_gaps),
        "Mean":      f"{pop_gaps.mean():.2f} y",
        "Std dev":   f"{pop_gaps.std():.2f} y",
        "Min":       f"{pop_gaps.min():.2f} y",
        "P25":       f"{np.percentile(pop_gaps, 25):.2f} y",
        "Median":    f"{np.median(pop_gaps):.2f} y",
        "P75":       f"{np.percentile(pop_gaps, 75):.2f} y",
        "Max":       f"{pop_gaps.max():.2f} y",
        "Client gap": f"{client_gap:+.2f} y",
        "Client percentile": f"{percentile:.0f}th",
    }
    st.table(pd.DataFrame.from_dict(stats, orient="index", columns=["Value"]))
