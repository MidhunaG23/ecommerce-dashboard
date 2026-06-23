"""
E-Commerce Analytics Dashboard - main entry point.

Run with:
    streamlit run app.py

The app works with ANY uploaded CSV/Excel file. It auto-detects column
roles, lets the user override the mapping, and adapts every chart and
filter to whatever data is actually present - never crashing on
unexpected or missing columns.
"""

import streamlit as st

from utils.data_loader import load_file, clean_dataframe
from utils.sample_data import generate_sample_data
from utils.column_detector import detect_columns, has_minimum_viable_data
from components.filters import render_sidebar_filters, render_column_mapping_editor
from pages_content import dashboard, product_analysis, customer_analysis, reports, about

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="E-Commerce Dashboard", page_icon="🛒", layout="wide")

st.markdown(
    """
    <style>
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e6e6e6;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🛒 E-Commerce Sales Analytics Dashboard")
st.caption("Upload any sales-style CSV/Excel file - the dashboard adapts automatically.")

# ---------------- DATA SOURCE SELECTION ----------------
st.sidebar.title("📁 Data Source")
use_sample = st.sidebar.toggle("Use sample dataset", value=False)

df = None
load_error = None

if use_sample:
    df = generate_sample_data()
else:
    uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        with st.spinner("Reading file..."):
            df, load_error = load_file(uploaded_file)

# ---------------- ERROR / EMPTY STATES ----------------
if df is None:
    if load_error:
        st.error(f"⚠️ {load_error}")
    else:
        st.info("👆 Upload a file or enable **Use sample dataset** in the sidebar to get started.")
    st.stop()

df = clean_dataframe(df)
col_map = detect_columns(df)

# ---------------- DATA PREVIEW ----------------
with st.expander("📄 Data Preview", expanded=False):
    st.dataframe(df.head(20), use_container_width=True)
    st.caption(f"{len(df)} rows x {len(df.columns)} columns detected.")

# ---------------- COLUMN MAPPING ----------------
col_map = render_column_mapping_editor(df, col_map)

if not has_minimum_viable_data(col_map):
    st.warning(
        "⚠️ We couldn't automatically detect enough usable columns "
        "(need at least one numeric metric like Sales/Profit and one "
        "category-like column such as Category or Product). "
        "Use **Column Mapping (Advanced)** in the sidebar to map them manually."
    )
    st.stop()

# ---------------- NAVIGATION ----------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Dashboard", "📦 Product Analysis", "👥 Customer Analysis", "📋 Reports", "ℹ️ About"],
)

# ---------------- FILTERS ----------------
filtered_df = render_sidebar_filters(df, col_map)

# ---------------- ROUTE TO PAGE ----------------
if page == "🏠 Dashboard":
    dashboard.render(filtered_df, col_map)
elif page == "📦 Product Analysis":
    product_analysis.render(filtered_df, col_map)
elif page == "👥 Customer Analysis":
    customer_analysis.render(filtered_df, col_map)
elif page == "📋 Reports":
    reports.render(filtered_df, col_map)
elif page == "ℹ️ About":
    about.render()

st.markdown("---")
st.caption("Built with Streamlit, Pandas, and Plotly")
