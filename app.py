import streamlit as st
from pathlib import Path

from frontend.components.sidebar import render_sidebar
from frontend.pages.research_home import render_research_home
from frontend.pages.research_results import render_research_results
from frontend.pages.document_upload import render_document_upload

st.set_page_config(
    page_title="NewsVault AI - Document Upload",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Initialize Page State
# Default to 'results' to show Figma design immediately
# -----------------------------
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "upload"

if "search_query" not in st.session_state:
    st.session_state["search_query"] = "What did we report about Company X in 2018?"


# -----------------------------
# Load CSS
# -----------------------------
css_path = Path(__file__).parent / "frontend" / "styles" / "main.css"

with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar
# -----------------------------
render_sidebar()


# -----------------------------
# Main Content Routing
# -----------------------------
if st.session_state["current_page"] == "results":
    render_research_results()
elif st.session_state["current_page"] == "upload":
    render_document_upload()
else:
    render_research_home()