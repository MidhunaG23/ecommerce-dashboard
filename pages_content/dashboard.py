"""Main dashboard overview page."""

import streamlit as st
from components.kpi import render_kpis
from components.charts import category_charts, trend_chart, region_chart
from utils.helpers import empty_state


def render(df, col_map):
    st.header("📊 Dashboard Overview")

    if df.empty:
        empty_state("No rows match the current filters. Try widening your filter selection.")
        return

    render_kpis(df, col_map)
    st.divider()

    category_col = col_map.get("category")
    metric_col = col_map.get("sales") or col_map.get("profit")
    if category_col and metric_col:
        top_cat = df.groupby(category_col)[metric_col].sum().idxmax()
        st.info(f"📊 Top performing category: **{top_cat}**")

    product_col = col_map.get("product")
    if product_col and metric_col:
        top_product = df.groupby(product_col)[metric_col].sum().idxmax()
        st.success(f"🔥 Best selling product: **{top_product}**")

    st.subheader("Category Performance")
    category_charts(df, col_map)

    st.subheader("Trend Over Time")
    trend_chart(df, col_map)

    st.subheader("Regional Performance")
    region_chart(df, col_map)
