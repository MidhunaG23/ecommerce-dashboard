"""Customer-focused analysis page."""

import streamlit as st
from components.charts import top_n_bar
from utils.helpers import empty_state, safe_nunique


def render(df, col_map):
    st.header("Customer Analysis")

    if df.empty:
        empty_state("No rows match the current filters.")
        return

    customer_col = col_map.get("customer")
    metric_col = col_map.get("sales") or col_map.get("profit")
    order_col = col_map.get("order_id")

    if not customer_col:
        empty_state("No customer column detected in this dataset.")
        return

    total_customers = safe_nunique(df, customer_col)
    st.metric("Unique Customers", f"{total_customers:,}")

    top_n_bar(df, customer_col, metric_col, "Top Customers by Sales", n=10)

    st.subheader("Customer Order Frequency")
    if order_col:
        freq = df.groupby(customer_col)[order_col].nunique().sort_values(ascending=False).head(10)
    else:
        freq = df[customer_col].value_counts().head(10)
    st.bar_chart(freq)
