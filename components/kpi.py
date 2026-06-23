"""KPI metric cards, adaptive to whichever columns are available."""

import streamlit as st
from utils.helpers import safe_sum, safe_nunique, format_currency


def render_kpis(df, col_map):
    """Render up to 4 KPI cards depending on what data is available."""
    sales_col = col_map.get("sales")
    profit_col = col_map.get("profit")
    order_col = col_map.get("order_id")

    total_sales = safe_sum(df, sales_col)
    total_profit = safe_sum(df, profit_col)
    total_orders = safe_nunique(df, order_col) if order_col else len(df)
    margin = (total_profit / total_sales * 100) if total_sales else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Sales", format_currency(total_sales) if sales_col else "N/A")
    col2.metric("📈 Total Profit", format_currency(total_profit) if profit_col else "N/A")
    col3.metric("📦 Total Orders", f"{total_orders:,}")
    margin_display = f"{margin:.2f}%" if sales_col and profit_col else "N/A"
    col4.metric("📊 Profit Margin", margin_display)
