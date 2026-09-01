import streamlit as st
from frontend.components.source_card import render_source_card
from frontend.components.evidence_card import render_evidence_modal


def clean_html(html_str: str) -> str:
    return " ".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_research_results():
    query_text = st.session_state.get("search_query", "What did we report about Company X in 2018?")
    if not query_text:
        query_text = "What did we report about Company X in 2018?"

    # Container wrapper for results view
    st.markdown('<div class="results-page-wrapper">', unsafe_allow_html=True)

    # 1. Back to Search Navigation
    col_back, _ = st.columns([2, 8])
    with col_back:
        if st.button("← Back to Search", key="back_to_search_btn"):
            st.session_state["current_page"] = "home"
            st.rerun()

    # 2. Original Query Header Card
    editing_query = st.session_state.get("editing_query", False)

    if editing_query:
        with st.form("edit_query_form"):
            new_query = st.text_input("Edit Query", value=query_text)
            if st.form_submit_button("Update Search"):
                st.session_state["search_query"] = new_query
                st.session_state["editing_query"] = False
                st.rerun()
    else:
        query_card_html = clean_html(f"""
        <div class="original-query-card">
            <div class="query-avatar-box">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
            </div>
            <div class="query-content">
                <div class="query-label">ORIGINAL QUERY</div>
                <div class="query-text">"{query_text}"</div>
            </div>
            <div class="query-edit-btn-wrapper">
        """)
        st.markdown(query_card_html, unsafe_allow_html=True)
        
        # Render pencil edit button inside card
        if st.button("✏️", key="btn_edit_query", help="Edit query"):
            st.session_state["editing_query"] = True
            st.rerun()
            
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # 3. Two-Column Layout (AI Synthesis & Primary Sources)
    col_left, col_right = st.columns([1.85, 1.0], gap="large")

    with col_left:
        # AI SYNTHESIS CARD
        synthesis_html = clean_html("""
        <div class="ai-synthesis-card">
            <div class="synthesis-header">
                <div class="synthesis-title">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 2L14.59 9.41L22 12L14.59 14.59L12 22L9.41 14.59L2 12L9.41 9.41L12 2Z"/>
                    </svg>
                    <span>AI SYNTHESIS</span>
                </div>
                <div class="confidence-badge">
                    <span class="confidence-dot">●</span> 98% Confidence
                </div>
            </div>

            <p class="synthesis-text">
                The company reported extensively on its expansion, financial performance, and industry impact based on archived reports. In 2018, Company X experienced significant milestones focused on aggressive global market penetration and organizational restructuring to support scaling.
            </p>

            <div class="bullet-points-container">
                <div class="bullet-points-title">KEY BULLET POINTS</div>

                <div class="bullet-item">
                    <div class="bullet-icon">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                        </svg>
                    </div>
                    <div class="bullet-text">
                        <strong>Global Expansion Initiative:</strong> Launched new operations in EMEA and APAC regions, driving a 24% increase in international revenue.
                    </div>
                </div>

                <div class="bullet-item">
                    <div class="bullet-icon">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                        </svg>
                    </div>
                    <div class="bullet-text">
                        <strong>Leadership Transition:</strong> The CEO highlighted operational efficiency and digital transformation as key strategic pillars during the Q3 earnings call.
                    </div>
                </div>

                <div class="bullet-item">
                    <div class="bullet-icon">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                        </svg>
                    </div>
                    <div class="bullet-text">
                        <strong>Financial Performance:</strong> The 2018 Annual Report confirmed a record-breaking fiscal year with net profits exceeding previous forecasts by 12%.
                    </div>
                </div>
            </div>

            <div class="synthesis-footer">
                <span class="meta-generated">Generated in 1.2s</span>
                <div class="action-buttons-group">
                    <button class="action-icon-btn" title="Copy synthesis">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                        </svg>
                    </button>
                    <button class="action-icon-btn" title="Good response">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
                        </svg>
                    </button>
                    <button class="action-icon-btn" title="Bad response">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h3a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-3"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        """)
        st.markdown(synthesis_html, unsafe_allow_html=True)

    with col_right:
        # PRIMARY SOURCES COLUMN
        st.markdown(clean_html("""
        <div class="primary-sources-header">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
            </svg>
            <span>PRIMARY SOURCES (3)</span>
        </div>
        """), unsafe_allow_html=True)

        sources_data = [
            {
                "id": "s1",
                "badge": "Article",
                "type": "article",
                "date": "July 12, 2018",
                "title": "Company X Expands Globally",
                "excerpt": "Company X today announced its expansion into EMEA and APAC regions with three new regional offices. International revenues are projected to increase by 24% year-over-year.",
                "relevance": "98%"
            },
            {
                "id": "s2",
                "badge": "Interview",
                "type": "interview",
                "date": "August 22, 2018",
                "title": "CEO Interview: The Road Ahead",
                "excerpt": "In an exclusive interview, the CEO outlined the strategic realignment focusing on operational efficiency, key digital transformation initiatives, and Q3 milestones.",
                "relevance": "94%"
            },
            {
                "id": "s3",
                "badge": "Report",
                "type": "report",
                "date": "December 18, 2018",
                "title": "Annual Report: Company X 2018",
                "excerpt": "The 2018 Annual Report confirms net profits exceeded forecasts by 12% following a record fiscal year marked by organizational restructuring and core market growth.",
                "relevance": "96%"
            }
        ]

        for s in sources_data:
            if render_source_card(s["id"], s["badge"], s["type"], s["date"], s["title"]):
                st.session_state["selected_evidence"] = s
                st.rerun()

    # 4. Render Evidence Modal if triggered
    selected = st.session_state.get("selected_evidence")
    if selected:
        render_evidence_modal(
            source_title=selected["title"],
            badge_label=selected["badge"],
            date_str=selected["date"],
            excerpt=selected["excerpt"],
            relevance=selected["relevance"]
        )

    st.markdown('</div>', unsafe_allow_html=True)
