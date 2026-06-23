"""About / info page."""

import streamlit as st


def render():
    st.header("About This Dashboard")
    st.write(
        "This is a dynamic E-Commerce Analytics Dashboard built with Streamlit, "
        "Pandas, and Plotly. Unlike a typical dashboard tied to one fixed dataset, "
        "this app automatically detects column roles (date, sales, profit, category, "
        "product, customer, region) from any uploaded CSV or Excel file, and adapts "
        "every chart, filter, and KPI to whatever data is actually present."
    )
    st.markdown(
        "Key capabilities:\n"
        "- Works with any reasonably structured CSV/Excel file\n"
        "- Manual column-mapping override when auto-detection guesses wrong\n"
        "- Graceful handling of missing columns, empty files, and bad formats\n"
        "- Sample dataset mode for instant exploration\n"
    )
    st.caption("Built with Streamlit, Pandas, and Plotly")
