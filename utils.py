import pandas as pd
import streamlit as st
import requests
import io
import trafilatura
import re

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def load_data():
    """
    Load consumer data from GitHub Excel file
    """
    try:
        # GitHub URL for the Excel file
        GITHUB_URL = "https://github.com/aditya-gupta-andc/Securepin/blob/6d06d3f715f14b8ec34c5d98d8f511f7b99ca702/Ghosi_IDF_Jan.xlsx"

        # Convert GitHub URL to raw content URL
        RAW_URL = GITHUB_URL.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

        # Fetch the file content
        response = requests.get(RAW_URL)
        response.raise_for_status()

        # Read Excel content from the response
        excel_content = io.BytesIO(response.content)
        df = pd.read_excel(excel_content)

        # Ensure ACCT_ID column exists
        if 'ACCT_ID' not in df.columns:
            raise ValueError("Required column 'ACCT_ID' not found in the Excel file")

        # Fill NaN values with empty string
        df = df.fillna('')

        return df

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch data from GitHub: {str(e)}")
    except pd.errors.EmptyDataError:
        raise Exception("The Excel file is empty")
    except Exception as e:
        raise Exception(f"Failed to load data: {str(e)}")

@st.cache_data
def get_all_account_ids(df):
    """
    Get all unique account IDs for autocomplete
    """
    return sorted(df['ACCT_ID'].astype(str).unique().tolist())

def get_consumer_full_report(df, consumer_id):
    """
    Get detailed report for a consumer
    """
    try:
        # Convert consumer_id to string for comparison
        consumer_id = str(consumer_id)
        consumer = df[df['ACCT_ID'].astype(str) == consumer_id].iloc[0]

        # Specific columns for each section
        account_cols = ['ACCT_ID', 'SUBSTATION', 'FEEDER', 'SUPPLY_TYPE']

        personal_cols = [col for col in df.columns if any(term in col.upper() for term in 
            ['NAME', 'DOB', 'GENDER', 'CONTACT', 'FATHER', 'MOBILE', 'ADDR', 'CITY', 'STATE', 'PIN', 'POSTAL'])]

        meter_cols = ['SERIAL_NBR', 'Jan_meter_read_remark', 'MTR_MAKE', 'MTR_NO_RECORDED', 'CLOSING_READING']

        # Get remaining columns for Other Details
        used_cols = set(account_cols + personal_cols + meter_cols)
        other_cols = [col for col in df.columns if col not in used_cols]

        # Create sections with column groupings
        sections = {
            'Account Information': account_cols,
            'Personal Information': personal_cols,
            'Meter Information': meter_cols,
            'Other Details': other_cols
        }

        # Build the full report
        full_report = {}
        for section, columns in sections.items():
            section_data = {}
            for col in columns:
                if col in df.columns:
                    value = consumer[col]
                    # Convert empty strings and NaN to "Not Available"
                    section_data[col] = "Not Available" if pd.isna(value) or value == '' else value
            if section_data:  # Only add sections that have data
                full_report[section] = section_data

        return full_report
    except (KeyError, IndexError):
        return None
    except Exception as e:
        st.error(f"Error getting full report: {str(e)}")
        return None