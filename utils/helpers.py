"""Small shared helper functions."""

import pandas as pd


def safe_sum(df: pd.DataFrame, col):
    """Sum a column safely, returning 0 if the column doesn't exist or is empty."""
    if col is None or col not in df.columns or df.empty:
        return 0
    return pd.to_numeric(df[col], errors="coerce").fillna(0).sum()


def safe_nunique(df: pd.DataFrame, col):
    """Count unique values safely."""
    if col is None or col not in df.columns or df.empty:
        return 0
    return df[col].nunique()


def format_currency(value, symbol="₹") -> str:
    """Format a number as currency with thousands separators."""
    try:
        return f"{symbol}{value:,.0f}"
    except (TypeError, ValueError):
        return f"{symbol}0"


def empty_state(message: str = "No data available for the current selection."):
    """Render a friendly empty-state block. Call inside a page when a
    chart/table has nothing to show."""
    import streamlit as st
    st.info(f"ℹ️ {message}")
