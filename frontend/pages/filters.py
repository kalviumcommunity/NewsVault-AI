import streamlit as st
from frontend.components.filter_panel import render_filter_panel


def clean_html(html_str: str) -> str:
    return " ".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_filters():
    # Ensure default session state values exist
    if "filter_date_range" not in st.session_state:
        st.session_state["filter_date_range"] = (2015, 2025)
    if "filter_type" not in st.session_state:
        st.session_state["filter_type"] = "All Types"
    if "filter_author" not in st.session_state:
        st.session_state["filter_author"] = "All Authors"
    if "filter_topic" not in st.session_state:
        st.session_state["filter_topic"] = "All Topics"
    if "filter_keywords" not in st.session_state:
        st.session_state["filter_keywords"] = ""

    # 1. Header Section
    header_html = clean_html("""
    <div class="filters-page-header">
        <div class="header-left">
            <h1 class="filters-title">FILTERS</h1>
            <p class="filters-subtitle">Refine your research parameters to isolate key insights.</p>
        </div>
        <div class="header-right">
            <button class="header-icon-btn" title="Notifications">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                    <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                </svg>
            </button>
            <div class="user-avatar-badge">JD</div>
        </div>
    </div>
    <div class="header-divider"></div>
    """)
    st.markdown(header_html, unsafe_allow_html=True)

    # 2. Main Content Split Layout
    left_col, right_col = st.columns([2.2, 1], gap="large")

    with left_col:
        render_filter_panel()

    with right_col:
        # Active State Card (Dark Navy)
        date_start, date_end = st.session_state["filter_date_range"]
        f_type = st.session_state["filter_type"]
        f_author = st.session_state["filter_author"]
        f_topic = st.session_state["filter_topic"]

        active_state_html = clean_html(f"""
        <div class="active-state-card">
            <div class="card-header">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
                <h3>Active State</h3>
            </div>
            <div class="active-state-rows">
                <div class="state-row">
                    <span class="state-label">Date Range</span>
                    <span class="state-value">{date_start} - {date_end}</span>
                </div>
                <div class="state-row">
                    <span class="state-label">Type</span>
                    <span class="state-value">{f_type}</span>
                </div>
                <div class="state-row">
                    <span class="state-label">Author</span>
                    <span class="state-value">{f_author}</span>
                </div>
                <div class="state-row">
                    <span class="state-label">Topic</span>
                    <span class="state-value">{f_topic}</span>
                </div>
            </div>
        </div>
        """)
        st.markdown(active_state_html, unsafe_allow_html=True)

        # Quick Filters Outer Card Container
        qf_container = st.container(border=True)
        with qf_container:
            st.markdown(clean_html("""
            <div class="quick-filters-header">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0F172A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                </svg>
                <h3>Quick Filters</h3>
            </div>
            """), unsafe_allow_html=True)

            q1, q2 = st.columns(2)
            with q1:
                if st.button("This Year", key="qf_this_year", use_container_width=True):
                    st.session_state["filter_date_range"] = (2025, 2025)
                    st.rerun()
            with q2:
                if st.button("Last 5 Years", key="qf_last_5_years", use_container_width=True):
                    st.session_state["filter_date_range"] = (2020, 2025)
                    st.rerun()

            q3, q4 = st.columns(2)
            with q3:
                if st.button("Articles Only", key="qf_articles_only", use_container_width=True):
                    st.session_state["filter_type"] = "Articles"
                    st.rerun()
            with q4:
                if st.button("Interviews", key="qf_interviews", use_container_width=True):
                    st.session_state["filter_type"] = "Interviews"
                    st.rerun()

            q5, _ = st.columns([1, 1])
            with q5:
                if st.button("Reports", key="qf_reports", use_container_width=True):
                    st.session_state["filter_type"] = "Reports"
                    st.rerun()
