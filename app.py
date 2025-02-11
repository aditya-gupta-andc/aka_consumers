import streamlit as st
import pandas as pd
from utils import load_data, get_consumer_full_report, get_all_account_ids
from styles import apply_styles

# Page config
st.set_page_config(
    page_title="Consumer Search Report",
    page_icon="🔍",
    layout="wide"
)

# Apply custom styles
apply_styles()

def main():
    # Header
    st.title("📊 Consumer Search Report")
    st.markdown("---")

    # Load data
    with st.spinner("Loading consumer database..."):
        try:
            df = load_data()
            st.success("Database loaded successfully!")
        except Exception as e:
            st.error(f"Error loading database: {str(e)}")
            return

    # Get all account IDs for autocomplete
    account_ids = get_all_account_ids(df)

    # Search section
    st.subheader("🔍 Search Consumer")

    # Initialize session state for search
    if 'previous_search' not in st.session_state:
        st.session_state.previous_search = ""

    # Text input for search with autocomplete
    search_input = st.text_input(
        "Enter Account ID",
        value="",
        help="Start typing to see suggestions",
        key="search_input"
    )

    # Show suggestions only when typing
    if search_input:
        # Filter suggestions based on input
        suggestions = [id for id in account_ids if str(id).startswith(search_input)]
        if suggestions:
            suggestion = st.selectbox(
                "Suggestions",
                suggestions,
                key="suggestion_box"
            )
            if suggestion:
                search_input = suggestion

    # Clear previous results if search input changes
    if search_input != st.session_state.previous_search:
        st.session_state.previous_search = search_input
        st.session_state.show_results = False

    # Search button
    if st.button("Search", key="search_button") and search_input:
        st.session_state.show_results = True

    # Only show results if search was performed
    if getattr(st.session_state, 'show_results', False) and search_input:
        # Search processing
        with st.spinner("Searching..."):
            full_report = get_consumer_full_report(df, search_input)

            if full_report:
                st.subheader("📑 Consumer Report")
                # Display full report directly with section headers
                for section, data in full_report.items():
                    st.markdown(f"### {section}")
                    # Create columns for better layout
                    cols = st.columns(2)
                    items = list(data.items())
                    mid = len(items) // 2

                    # First column
                    for key, value in items[:mid]:
                        cols[0].write(f"**{key}:** {value}")

                    # Second column
                    for key, value in items[mid:]:
                        cols[1].write(f"**{key}:** {value}")

                    st.markdown("---")  # Add separator between sections
            else:
                st.warning("⚠️ No consumer found with the provided Account ID")

    # Help section
    with st.sidebar:
        st.header("ℹ️ Help")
        st.markdown("""
        **How to use:**
        1. Start typing the Account ID
        2. Select from suggested IDs or continue typing
        3. Click Search to view consumer information

        **Need assistance?**
        Contact support at support@company.com
        """)

if __name__ == "__main__":
    main()