"""
Dynamic sidebar filters.

Filters are only rendered for roles that were actually detected in the
dataset, so the sidebar adapts to whatever file the user uploads.
"""

import pandas as pd
import streamlit as st


def render_column_mapping_editor(df: pd.DataFrame, col_map: dict) -> dict:
    """
    Let the user manually override auto-detected columns.
    Returns a (possibly edited) copy of col_map.
    """
    with st.sidebar.expander("⚙️ Column Mapping (Advanced)", expanded=False):
        st.caption("Auto-detected columns. Override any that look wrong.")
        columns = ["(None)"] + list(df.columns)
        new_map = dict(col_map)

        labels = {
            "date": "Date column",
            "sales": "Sales / Revenue column",
            "profit": "Profit column",
            "quantity": "Quantity column",
            "category": "Category column",
            "product": "Product column",
            "customer": "Customer column",
            "region": "Region column",
            "order_id": "Order ID column",
        }

        for role, label in labels.items():
            current = col_map.get(role)
            default_index = columns.index(current) if current in columns else 0
            choice = st.selectbox(label, columns, index=default_index, key=f"map_{role}")
            new_map[role] = None if choice == "(None)" else choice

    return new_map


def render_sidebar_filters(df: pd.DataFrame, col_map: dict):
    """
    Render filters for whichever columns are present, and return the
    filtered dataframe.
    """
    st.sidebar.header("🔍 Filters")
    filtered_df = df.copy()

    search_text = st.sidebar.text_input("🔎 Global Search", help="Searches across all columns")
    if search_text:
        mask = filtered_df.apply(
            lambda col: col.astype(str).str.contains(search_text, case=False, na=False)
        )
        filtered_df = filtered_df[mask.any(axis=1)]

    category_col = col_map.get("category")
    if category_col and category_col in filtered_df.columns:
        options = sorted(df[category_col].dropna().astype(str).unique())
        if 0 < len(options) <= 100:
            selected = st.sidebar.multiselect("Category", options, default=options)
            filtered_df = filtered_df[filtered_df[category_col].astype(str).isin(selected)]

    region_col = col_map.get("region")
    if region_col and region_col in filtered_df.columns:
        options = sorted(df[region_col].dropna().astype(str).unique())
        if 0 < len(options) <= 100:
            selected = st.sidebar.multiselect("Region", options, default=options)
            filtered_df = filtered_df[filtered_df[region_col].astype(str).isin(selected)]

    date_col = col_map.get("date")
    if date_col and date_col in filtered_df.columns:
        parsed_dates = pd.to_datetime(filtered_df[date_col], errors="coerce")
        if parsed_dates.notna().any():
            filtered_df = filtered_df.assign(**{date_col: parsed_dates})
            min_date, max_date = parsed_dates.min(), parsed_dates.max()
            start_date, end_date = st.sidebar.date_input(
                "Date range", value=(min_date.date(), max_date.date())
            ) if min_date.date() != max_date.date() else (min_date.date(), max_date.date())
            filtered_df = filtered_df[
                (filtered_df[date_col] >= pd.to_datetime(start_date))
                & (filtered_df[date_col] <= pd.to_datetime(end_date))
            ]

    product_col = col_map.get("product")
    if product_col and product_col in filtered_df.columns:
        options = ["All"] + sorted(filtered_df[product_col].dropna().astype(str).unique())
        if len(options) > 1:
            choice = st.sidebar.selectbox("Product", options)
            if choice != "All":
                filtered_df = filtered_df[filtered_df[product_col].astype(str) == choice]

    if st.sidebar.button("🔄 Reset Filters"):
        st.rerun()

    return filtered_df
