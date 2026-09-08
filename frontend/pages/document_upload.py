import streamlit as st
from frontend.components.upload_box import render_upload_box


def clean_html(html_str: str) -> str:
    return " ".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_document_upload():
    # Page Header matching main.css design
    header_html = clean_html("""
    <div class="document-upload-page">
        <div class="upload-page-header">
            <h1 class="upload-page-title">UPLOAD ARCHIVE DOCUMENTS</h1>
            <p class="upload-page-subtitle">Securely upload documents for AI processing and analysis.</p>
        </div>
    </div>
    """)
    st.markdown(header_html, unsafe_allow_html=True)

    # Render actual upload card component
    render_upload_box()