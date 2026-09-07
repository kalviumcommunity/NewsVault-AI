import streamlit as st


def clean_html(html_str: str) -> str:
    return " ".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_filter_panel():
    # Ensure default session state values
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

    # Parameter Configuration Outer White Card Box ("outbox")
    panel_container = st.container(border=True)
    with panel_container:
        # 1. Panel Header
        st.markdown(clean_html("""
        <div class="panel-header-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
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
            <h2>Parameter Configuration</h2>
        </div>
        <div class="panel-divider"></div>
        """), unsafe_allow_html=True)

        # 2. Temporal Range Unified Card
        curr_start, curr_end = st.session_state["filter_date_range"]
        
        # Temporal Box Title
        st.markdown(clean_html(f"""
        <div class="temporal-card-box">
            <span class="temporal-title">Temporal Range ({curr_start} - {curr_end})</span>
        </div>
        """), unsafe_allow_html=True)

        # Streamlit Range Slider (handles 2015 and 2025 cleanly)
        selected_range = st.slider(
            "Temporal Range",
            min_value=2015,
            max_value=2025,
            value=st.session_state["filter_date_range"],
            label_visibility="collapsed",
            key="temp_range_slider"
        )

        # Temporal Box AI Hint Footer
        st.markdown(clean_html("""
        <div class="temporal-card-box-bottom">
            <span>AI Suggests narrowing to 2018-2022 based on 'Technology' trends.</span>
        </div>
        """), unsafe_allow_html=True)

        # 3. Filter Controls Grid
        col1, col2 = st.columns(2)

        with col1:
            type_options = ["All Types", "Articles", "Reports", "Interviews", "News"]
            type_idx = type_options.index(st.session_state["filter_type"]) if st.session_state["filter_type"] in type_options else 0
            selected_type = st.selectbox(
                "Content Type",
                options=type_options,
                index=type_idx,
                key="select_content_type"
            )

            topic_options = ["All Topics", "Technology", "Finance", "Healthcare", "Policy"]
            topic_idx = topic_options.index(st.session_state["filter_topic"]) if st.session_state["filter_topic"] in topic_options else 0
            selected_topic = st.selectbox(
                "Primary Topic",
                options=topic_options,
                index=topic_idx,
                key="select_primary_topic"
            )

        with col2:
            author_options = ["All Authors", "John Doe", "Jane Smith", "Reuters", "TechCrunch"]
            author_idx = author_options.index(st.session_state["filter_author"]) if st.session_state["filter_author"] in author_options else 0
            selected_author = st.selectbox(
                "Author / Source",
                options=author_options,
                index=author_idx,
                key="select_author_source"
            )

            selected_keywords = st.text_input(
                "Semantic Keywords",
                value=st.session_state["filter_keywords"],
                placeholder="Enter keywords...",
                key="input_semantic_keywords"
            )

        st.markdown('<div class="panel-divider" style="margin-top: 20px; margin-bottom: 20px;"></div>', unsafe_allow_html=True)

        # 4. Action Buttons Footer
        btn_col1, btn_col2 = st.columns([1, 1])

        with btn_col1:
            if st.button("Clear Filters", key="btn_clear_filters", type="secondary", use_container_width=True):
                st.session_state["filter_date_range"] = (2015, 2025)
                st.session_state["filter_type"] = "All Types"
                st.session_state["filter_author"] = "All Authors"
                st.session_state["filter_topic"] = "All Topics"
                st.session_state["filter_keywords"] = ""
                st.rerun()

        with btn_col2:
            if st.button("✨ Apply Filters", key="btn_apply_filters", type="primary", use_container_width=True):
                st.session_state["filter_date_range"] = selected_range
                st.session_state["filter_type"] = selected_type
                st.session_state["filter_author"] = selected_author
                st.session_state["filter_topic"] = selected_topic
                st.session_state["filter_keywords"] = selected_keywords
                st.rerun()
