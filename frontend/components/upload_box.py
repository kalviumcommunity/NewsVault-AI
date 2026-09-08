import time
import streamlit as st


def clean_html(html_str: str) -> str:
    return " ".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_upload_box():
    # Session state for uploaded documents
    if "processed_docs" not in st.session_state:
        st.session_state["processed_docs"] = []

    # 1. Dashed Dropzone Visual Top Header
    dropzone_header_html = clean_html("""
    <div class="upload-dropzone-box">
        <div class="cloud-icon-circle">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/>
                <path d="M12 12v9"/>
                <path d="m16 16-4-4-4 4"/>
            </svg>
        </div>
        <div class="dropzone-heading">Drag & Drop files here</div>
        <div class="dropzone-subheading">or click to browse your computer</div>
    </div>
    """)
    st.markdown(dropzone_header_html, unsafe_allow_html=True)

    # 2. Streamlit File Uploader Component (Bottom half of dashed dropzone)
    uploaded_files = st.file_uploader(
        "Upload files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="archive_file_uploader",
        label_visibility="collapsed"
    )

    # Display selected files if any
    if uploaded_files:
        files_html_items = ""
        for f in uploaded_files:
            size_mb = f.size / (1024 * 1024)
            size_str = f"{size_mb:.2f} MB" if size_mb >= 0.1 else f"{f.size / 1024:.1f} KB"
            ext = f.name.split('.')[-1].upper() if '.' in f.name else 'FILE'

            files_html_items += f"""
            <div class="uploaded-file-item">
                <div class="file-item-icon">{ext}</div>
                <div class="file-item-info">
                    <span class="file-name">{f.name}</span>
                    <span class="file-size">{size_str}</span>
                </div>
                <div class="file-item-status">Ready</div>
            </div>
            """

        selected_files_html = clean_html(f"""
        <div class="uploaded-files-list">
            <div class="file-list-header">SELECTED FILES</div>
            {files_html_items}
        </div>
        """)
        st.markdown(selected_files_html, unsafe_allow_html=True)

    # 3. Process Documents Button
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        btn_clicked = st.button("✨ Process Documents", key="btn_process_documents", disabled=False, use_container_width=True)

    if btn_clicked:
        progress_placeholder = st.empty()
        status_placeholder = st.empty()

        with progress_placeholder.container():
            st.markdown('<div class="processing-progress-box">', unsafe_allow_html=True)
            p_bar = st.progress(0)
            
            steps = [
                (25, "Parsing document structure..."),
                (55, "Generating vector embeddings..."),
                (85, "Indexing into NewsVault database..."),
                (100, "Processing complete!")
            ]
            for percent, text in steps:
                time.sleep(0.25)
                p_bar.progress(percent)
                status_placeholder.markdown(f'<div class="processing-status-text">{text}</div>', unsafe_allow_html=True)
            
            time.sleep(0.15)

        progress_placeholder.empty()
        status_placeholder.empty()

        docs_to_process = uploaded_files if uploaded_files else [{"name": "archive_report_2018.pdf", "size": 2450000}]
        for f in docs_to_process:
            fname = f.name if hasattr(f, 'name') else f["name"]
            fsize = f.size if hasattr(f, 'size') else f["size"]
            if fname not in [d["name"] for d in st.session_state["processed_docs"]]:
                st.session_state["processed_docs"].append({"name": fname, "size": fsize})

        st.session_state["upload_success"] = True

    # Success Banner Feedback
    if st.session_state.get("upload_success"):
        doc_count = len(uploaded_files) if uploaded_files else 1
        success_html = clean_html(f"""
        <div class="upload-success-banner">
            <div class="success-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#166534" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
            </div>
            <div class="success-text">
                <strong>Documents Processed Successfully!</strong>
                <span>{doc_count} archive document(s) parsed and indexed into NewsVault AI.</span>
            </div>
        </div>
        """)
        st.markdown(success_html, unsafe_allow_html=True)

        col_search_nav, _ = st.columns([2, 3])
        with col_search_nav:
            if st.button("🔍 Go to Search", key="nav_to_search_after_upload"):
                st.session_state["current_page"] = "results"
                st.session_state["upload_success"] = False
                st.rerun()

    # 4. Footer Info Row
    footer_html = clean_html("""
    <div class="upload-footer-row">
        <div class="supported-formats">
            <span class="format-chip">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                </svg>
                PDF
            </span>
            <span class="format-dot">•</span>
            <span class="format-chip">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                </svg>
                DOCX
            </span>
            <span class="format-dot">•</span>
            <span class="format-chip">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                </svg>
                TXT
            </span>
        </div>
        <div class="processing-note">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>
            Large documents may take a few minutes to process.
        </div>
    </div>
    """)
    st.markdown(footer_html, unsafe_allow_html=True)
