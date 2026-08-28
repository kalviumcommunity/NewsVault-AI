import streamlit as st
from pathlib import Path

from frontend.components.sidebar import render_sidebar
from frontend.pages.research_home import render_research_home


st.set_page_config(
    page_title="NewsVault AI",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)


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
# Research Home
# -----------------------------

render_research_home()