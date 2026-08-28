import streamlit as st

from frontend.components.search_bar import render_search_bar


def clean_html(html_str: str) -> str:
    return " ".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_research_home():
    hero_html = clean_html("""
    <div class="research-page">
        <div class="hero-container">
            <div class="hero-content">
                <div class="document-icon-wrapper">
                    <div class="document-icon-box">
                        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                            <polyline points="14 2 14 8 20 8"></polyline>
                            <line x1="16" y1="13" x2="8" y2="13"></line>
                            <line x1="16" y1="17" x2="8" y2="17"></line>
                            <polyline points="10 9 9 9 8 9"></polyline>
                        </svg>
                        <div class="sparkle-badge">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="#0F172A">
                                <path d="M12 0L14.59 9.41L24 12L14.59 14.59L12 24L9.41 14.59L0 12L9.41 9.41L12 0Z"/>
                            </svg>
                        </div>
                    </div>
                </div>

                <h1 class="hero-title">NEWSVAULT AI</h1>

                <p class="hero-subtitle">
                    AI-Powered Journalism Research Assistant
                </p>

                <p class="hero-description">
                    Ask questions about your archive and get accurate answers with supporting sources.
                </p>
            </div>
        </div>
    </div>
    """)

    st.markdown(hero_html, unsafe_allow_html=True)

    question, search_clicked = render_search_bar()

    if search_clicked and question.strip():
        st.session_state["search_query"] = question
        try:
            st.switch_page("pages/research_results.py")
        except Exception:
            st.info(f"Searching for: {question}")