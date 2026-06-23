"""Full report / data export page."""

import streamlit as st
from utils.helpers import empty_state


def render(df, col_map):
    st.header("Reports")

    if df.empty:
        empty_state("No rows match the current filters.")
        return

    st.subheader("Filtered Data")
    st.dataframe(df, use_container_width=True)

    st.subheader("Data Quality Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", len(df))
    c2.metric("Columns", len(df.columns))
    c3.metric("Missing Cells", int(df.isnull().sum().sum()))

    with st.expander("Missing Values by Column"):
        st.write(df.isnull().sum())

    csv = df.to_csv(index=False)
    st.download_button(
        "Download Filtered Data as CSV",
        csv,
        file_name="filtered_report.csv",
        mime="text/csv",
    )
