import streamlit as st


def clean_html(html_str: str) -> str:
    return " ".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_upload_box():
    # Outer Card Container using st.container with key="upload_card_box"
    with st.container(key="upload_card_box"):
        # 1. Custom Visual Dashed Dropzone Header (Icon + Titles)
        dropzone_header_html = clean_html("""
        <div class="upload-dropzone-dashed-box">
            <div class="upload-cloud-icon-circle">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
            </div>
            <div class="upload-dropzone-title">Drag & Drop files here</div>
            <div class="upload-dropzone-subtitle">or click to browse your computer</div>
        """)
        st.markdown(dropzone_header_html, unsafe_allow_html=True)

        # 2. Native File Uploader Component (Renders Browse button inside dropzone)
        uploaded_files = st.file_uploader(
            "Browse Files",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="archive_doc_uploader"
        )

        # Close dashed box container
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # 3. Full-width Primary Process Documents Button
        if st.button("✨ Process Documents", key="btn_process_documents", use_container_width=True):
            if uploaded_files:
                with st.spinner("Processing documents for AI ingestion..."):
                    file_names = ", ".join([f.name for f in uploaded_files])
                    st.success(f"Successfully processed {len(uploaded_files)} document(s): {file_names}")
            else:
                st.warning("Please select or drop at least one document to process.")

        # 4. Card Footer Metadata Row (Supported Formats & Notice)
        footer_html = clean_html("""
        <div class="upload-card-footer">
            <div class="format-badges-group">
                <span class="format-pill-badge">📄 PDF</span>
                <span class="format-dot-separator">•</span>
                <span class="format-pill-badge">📄 DOCX</span>
                <span class="format-dot-separator">•</span>
                <span class="format-pill-badge">📄 TXT</span>
            </div>
            <div class="upload-notice-text">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="16" x2="12" y2="12"></line>
                    <line x1="12" y1="8" x2="12.01" y2="8"></line>
                </svg>
                <span>Large documents may take a few minutes to process.</span>
            </div>
        </div>
        """)
        st.markdown(footer_html, unsafe_allow_html=True)
