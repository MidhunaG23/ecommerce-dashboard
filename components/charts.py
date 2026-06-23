"""
Adaptive Plotly chart builders.

Each function checks whether the columns it needs exist before rendering,
and falls back to an empty-state message otherwise.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.helpers import empty_state


def category_charts(df, col_map):
    """Bar + pie chart of the chosen metric grouped by category."""
    category_col = col_map.get("category")
    metric_col = col_map.get("sales") or col_map.get("profit")

    if not category_col or not metric_col or df.empty:
        empty_state("Not enough data to show category breakdown.")
        return

    grouped = df.groupby(category_col)[metric_col].sum().reset_index()
    if grouped.empty:
        empty_state("No category data matches the current filters.")
        return

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(grouped, x=category_col, y=metric_col, color=category_col,
                      title=f"{metric_col} by {category_col}")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.pie(grouped, names=category_col, values=metric_col,
                       title=f"{metric_col} Distribution")
        st.plotly_chart(fig2, use_container_width=True)


def trend_chart(df, col_map):
    """Line chart of the metric over time, if a date column is available."""
    date_col = col_map.get("date")
    metric_col = col_map.get("sales") or col_map.get("profit")

    if not date_col or not metric_col or df.empty:
        empty_state("No date column detected - trend chart unavailable.")
        return

    temp = df.copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
    temp = temp.dropna(subset=[date_col])
    if temp.empty:
        empty_state("No valid dates found for trend analysis.")
        return

    temp["period"] = temp[date_col].dt.to_period("M").astype(str)
    monthly = temp.groupby("period")[metric_col].sum().reset_index()
    fig = px.line(monthly, x="period", y=metric_col, markers=True,
                  title=f"Monthly {metric_col} Trend")
    st.plotly_chart(fig, use_container_width=True)


def region_chart(df, col_map):
    """Bar chart of metric by region, if available."""
    region_col = col_map.get("region")
    metric_col = col_map.get("sales") or col_map.get("profit")

    if not region_col or not metric_col or df.empty:
        empty_state("No region column detected.")
        return

    grouped = df.groupby(region_col)[metric_col].sum().reset_index().sort_values(metric_col, ascending=False)
    if grouped.empty:
        empty_state("No region data matches the current filters.")
        return

    fig = px.bar(grouped, x=region_col, y=metric_col, color=region_col,
                  title=f"{metric_col} by Region")
    st.plotly_chart(fig, use_container_width=True)


def top_n_bar(df, group_col, metric_col, title, n=10):
    """Generic horizontal bar chart of top-N groups by a metric."""
    if not group_col or not metric_col or df.empty:
        empty_state(f"Not enough data to compute {title}.")
        return

    grouped = (
        df.groupby(group_col)[metric_col]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )
    if grouped.empty:
        empty_state(f"No data matches the current filters for {title}.")
        return

    fig = px.bar(grouped, x=metric_col, y=group_col, orientation="h", title=title)
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)
