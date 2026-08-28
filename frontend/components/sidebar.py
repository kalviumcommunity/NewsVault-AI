import streamlit as st


def clean_html(html_str: str) -> str:
    return " ".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_sidebar():
    with st.sidebar:
        sidebar_html = clean_html("""
        <div class="sidebar-container">
            <div class="sidebar-brand">
                <div class="brand-icon">N</div>
                <span class="brand-name">NewsVault AI</span>
            </div>

            <div class="sidebar-navigation">
                <div class="sidebar-item active">
                    <span class="sidebar-icon">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                            <polyline points="9 22 9 12 15 12 15 22"></polyline>
                        </svg>
                    </span>
                    <span class="sidebar-text">Home</span>
                </div>

                <div class="sidebar-item">
                    <span class="sidebar-icon">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="11" cy="11" r="8"></circle>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                        </svg>
                    </span>
                    <span class="sidebar-text">Search</span>
                </div>

                <div class="sidebar-item">
                    <span class="sidebar-icon">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                            <polyline points="14 2 14 8 20 8"></polyline>
                            <line x1="12" y1="18" x2="12" y2="12"></line>
                            <line x1="9" y1="15" x2="12" y2="12"></line>
                            <line x1="15" y1="15" x2="12" y2="12"></line>
                        </svg>
                    </span>
                    <span class="sidebar-text">Upload</span>
                </div>

                <div class="sidebar-item">
                    <span class="sidebar-icon">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="4" y1="21" x2="4" y2="14"></line>
                            <line x1="4" y1="10" x2="4" y2="3"></line>
                            <line x1="12" y1="21" x2="12" y2="12"></line>
                            <line x1="12" y1="8" x2="12" y2="3"></line>
                            <line x1="20" y1="21" x2="20" y2="16"></line>
                            <line x1="20" y1="12" x2="20" y2="3"></line>
                            <line x1="1" y1="14" x2="7" y2="14"></line>
                            <line x1="9" y1="8" x2="15" y2="8"></line>
                            <line x1="17" y1="16" x2="23" y2="16"></line>
                        </svg>
                    </span>
                    <span class="sidebar-text">Filters</span>
                </div>
            </div>

            <div class="sidebar-spacer"></div>

            <div class="sidebar-footer">
                <div class="sidebar-item logout-item">
                    <span class="sidebar-icon">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                            <polyline points="16 17 21 12 16 7"></polyline>
                            <line x1="21" y1="12" x2="9" y2="12"></line>
                        </svg>
                    </span>
                    <span class="sidebar-text">Logout</span>
                </div>
            </div>
        </div>
        """)
        st.markdown(sidebar_html, unsafe_allow_html=True)