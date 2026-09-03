import streamlit as st
from frontend.components.upload_box import render_upload_box


def clean_html(html_str: str) -> str:
    return " ".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_document_upload():
    st.markdown('<div class="document-upload-page">', unsafe_allow_html=True)

    # 1. Page Header Section
    header_html = clean_html("""
    <div class="upload-page-header">
        <h1 class="upload-page-title">UPLOAD ARCHIVE DOCUMENTS</h1>
        <p class="upload-page-subtitle">Securely upload documents for AI processing and analysis.</p>
    </div>
    """)
    st.markdown(header_html, unsafe_allow_html=True)

    # 2. Upload Box Component
    render_upload_box()

    st.markdown('</div>', unsafe_allow_html=True)
