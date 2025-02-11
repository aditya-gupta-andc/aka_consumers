import streamlit as st

def apply_styles():
    """
    Apply custom CSS styles to the Streamlit app
    """
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton button {
            width: 100%;
            background-color: #0066cc;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            margin-top: 1rem;
        }
        .stTextInput input {
            border-radius: 5px;
        }
        .stAlert {
            border-radius: 5px;
        }
        .stExpander {
            border-radius: 5px;
            margin-bottom: 1rem;
        }
        .css-1d391kg {
            padding: 2rem;
        }
        h1 {
            color: #0066cc;
        }
        h2 {
            margin-top: 2rem;
        }
        hr {
            margin: 2rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
