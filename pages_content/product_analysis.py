"""Product-focused analysis page."""

import streamlit as st
from components.charts import top_n_bar
from utils.helpers import empty_state


def render(df, col_map):
    st.header("Product Analysis")

    if df.empty:
        empty_state("No rows match the current filters.")
        return

    product_col = col_map.get("product")
    metric_col = col_map.get("sales") or col_map.get("profit")
    qty_col = col_map.get("quantity")

    if not product_col:
        empty_state("No product column detected in this dataset.")
        return

    c1, c2 = st.columns(2)
    with c1:
        top_n_bar(df, product_col, metric_col, "Top Products by Sales", n=10)
    with c2:
        if qty_col:
            top_n_bar(df, product_col, qty_col, "Top Products by Quantity Sold", n=10)
        else:
            empty_state("No quantity column detected.")

    st.subheader("Full Product Breakdown")
    if metric_col:
        breakdown = df.groupby(product_col)[metric_col].agg(["sum", "mean", "count"]).reset_index()
        breakdown.columns = [product_col, "Total " + metric_col, "Avg " + metric_col, "Order Count"]
        st.dataframe(breakdown.sort_values("Total " + metric_col, ascending=False), use_container_width=True)
