import pandas as pd
import streamlit as st
#Required columns
REQUIRED_COLUMNS=[
    "review",
    "rating",
    "product",
    "date",
    "region"
]


def load_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        return df

    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return None
    
def validate_columns(df):
    missing = []
    
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            missing.append(col)
            
    return missing