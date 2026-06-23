"""
Safe file loading for CSV and Excel uploads.

All loading is wrapped so the app NEVER crashes on a bad file - every
function returns (dataframe_or_None, error_message_or_None).
"""

import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_file(uploaded_file):
    """
    Load an uploaded CSV or Excel file into a DataFrame.

    Returns:
        (df, error_message)
        df is None if loading failed; error_message is None if it succeeded.
    """
    if uploaded_file is None:
        return None, "No file provided."

    filename = uploaded_file.name.lower()

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Unsupported file format. Please upload a .csv or .xlsx file."
    except pd.errors.EmptyDataError:
        return None, "The uploaded file is empty."
    except pd.errors.ParserError:
        return None, "Could not parse the file. It may be corrupted or in an unexpected format."
    except Exception as e:
        return None, f"Could not read the file: {e}"

    is_valid, validation_error = validate_dataframe(df)
    if not is_valid:
        return None, validation_error

    return df, None


def validate_dataframe(df: pd.DataFrame):
    """Basic sanity checks on a loaded dataframe."""
    if df is None:
        return False, "File could not be loaded."
    if df.empty:
        return False, "The uploaded file has no rows of data."
    if len(df.columns) < 2:
        return False, "The uploaded file needs at least two columns to build a dashboard."
    df.dropna(how="all", inplace=True)
    df.dropna(axis=1, how="all", inplace=True)
    if df.empty:
        return False, "After removing empty rows, no data remains."
    return True, None


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Light cleaning applied to any uploaded dataset before use."""
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()
    return df
