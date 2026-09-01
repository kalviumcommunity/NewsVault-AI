import streamlit as st


def clean_html(html_str: str) -> str:
    return " ".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_sidebar():
    current_page = st.session_state.get("current_page", "results")

    with st.sidebar:
        brand_html = clean_html("""
        <div class="sidebar-brand">
            <div class="brand-icon">N</div>
            <span class="brand-name">NewsVault AI</span>
        </div>
        """)
        st.markdown(brand_html, unsafe_allow_html=True)

        # Home button
        home_key = "nav_home_active" if current_page == "home" else "nav_home_inactive"
        if st.button("🏠  Home", key=home_key, use_container_width=True):
            st.session_state["current_page"] = "home"
            st.rerun()

        # Search button
        search_key = "nav_search_active" if current_page == "results" else "nav_search_inactive"
        if st.button("🔍  Search", key=search_key, use_container_width=True):
            st.session_state["current_page"] = "results"
            st.rerun()

        if st.button("📤  Upload", key="nav_upload_btn", use_container_width=True):
            st.info("Document Upload page coming soon")

        if st.button("🎛️  Filters", key="nav_filters_btn", use_container_width=True):
            st.info("Filters panel coming soon")

        st.markdown('<div class="sidebar-spacer" style="height: 180px;"></div>', unsafe_allow_html=True)

        if st.button("🚪  Logout", key="nav_logout_btn", use_container_width=True):
            st.success("Logged out")