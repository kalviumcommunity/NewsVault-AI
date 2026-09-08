import streamlit as st

from frontend.components.source_card import render_source_card
from frontend.components.evidence_card import render_evidence_modal
from backend.services.rag_service import answer_question


def clean_html(html_str: str) -> str:
    return " ".join(
        line.strip()
        for line in html_str.splitlines()
        if line.strip()
    )


def render_research_results():
    query_text = st.session_state.get(
        "search_query",
        "What did we report about Company X in 2018?"
    )

    if not query_text:
        query_text = "What did we report about Company X in 2018?"

    # --------------------------------------------------
    # Generate RAG answer
    # --------------------------------------------------
    if "rag_answer" not in st.session_state:
        with st.spinner("Researching the archive..."):
            try:
                st.session_state["rag_answer"] = answer_question(query_text)
            except Exception as e:
                st.session_state["rag_answer"] = (
                    f"Unable to generate an answer: {e}"
                )

    answer = st.session_state["rag_answer"]

    # --------------------------------------------------
    # Container wrapper
    # --------------------------------------------------
    st.markdown(
        '<div class="results-page-wrapper">',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Back to Search Navigation
    # --------------------------------------------------
    col_back, _ = st.columns([2, 8])

    with col_back:
        if st.button(
            "← Back to Search",
            key="back_to_search_btn"
        ):
            st.session_state["current_page"] = "home"
            st.session_state.pop("rag_answer", None)
            st.rerun()

    # --------------------------------------------------
    # Original Query Header Card
    # --------------------------------------------------
    editing_query = st.session_state.get(
        "editing_query",
        False
    )

    if editing_query:

        with st.form("edit_query_form"):

            new_query = st.text_input(
                "Edit Query",
                value=query_text
            )

            if st.form_submit_button("Update Search"):

                st.session_state["search_query"] = new_query
                st.session_state["editing_query"] = False
                st.session_state.pop("rag_answer", None)

                st.rerun()

    else:

        query_card_html = clean_html(
            f"""
            <div class="original-query-card">
                <div class="query-avatar-box">
                    <svg width="20" height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="#475569"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round">

                        <path d="M20 21v-2a4 4 0 0 0-4-4H8
                        a4 4 0 0 0-4 4v2"></path>

                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                </div>

                <div class="query-content">
                    <div class="query-label">
                        ORIGINAL QUERY
                    </div>

                    <div class="query-text">
                        "{query_text}"
                    </div>
                </div>

                <div class="query-edit-btn-wrapper">
            """
        )

        st.markdown(
            query_card_html,
            unsafe_allow_html=True
        )

        if st.button(
            "✏️",
            key="btn_edit_query",
            help="Edit query"
        ):
            st.session_state["editing_query"] = True
            st.rerun()

        st.markdown(
            "</div></div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<div style='height: 16px;'></div>",
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Two Column Layout
    # --------------------------------------------------
    col_left, col_right = st.columns(
        [1.85, 1.0],
        gap="large"
    )

    # ==================================================
    # LEFT COLUMN - AI SYNTHESIS
    # ==================================================
    with col_left:

        synthesis_header = clean_html(
            """
            <div class="ai-synthesis-card">

                <div class="synthesis-header">

                    <div class="synthesis-title">

                        <svg width="18" height="18"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="#2563EB"
                            stroke-width="2.5"
                            stroke-linecap="round"
                            stroke-linejoin="round">

                            <path d="M12 2L14.59 9.41L22 12
                            L14.59 14.59L12 22L9.41 14.59
                            L2 12L9.41 9.41L12 2Z"/>

                        </svg>

                        <span>AI SYNTHESIS</span>

                    </div>

                    <div class="confidence-badge">
                        <span class="confidence-dot">●</span>
                        Archive Grounded
                    </div>

                </div>
            """
        )

        st.markdown(
            synthesis_header,
            unsafe_allow_html=True
        )

        # ----------------------------------------------
        # REAL RAG ANSWER
        # ----------------------------------------------
        st.markdown(answer)

        # ----------------------------------------------
        # Footer
        # ----------------------------------------------
        st.markdown(
            clean_html(
                """
                <div class="synthesis-footer">

                    <span class="meta-generated">
                        Generated using NewsVault AI
                    </span>

                </div>

                </div>
                """
            ),
            unsafe_allow_html=True
        )

    # ==================================================
    # RIGHT COLUMN - PRIMARY SOURCES
    # ==================================================
    with col_right:

        st.markdown(
            clean_html(
                """
                <div class="primary-sources-header">

                    <svg width="16" height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="#475569"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round">

                        <path d="M14 2H6a2 2 0 0 0-2 2v16
                        a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z">
                        </path>

                        <polyline points="14 2 14 8 20 8">
                        </polyline>

                        <line x1="16" y1="13"
                            x2="8" y2="13"></line>

                        <line x1="16" y1="17"
                            x2="8" y2="17"></line>

                    </svg>

                    <span>PRIMARY SOURCES</span>

                </div>
                """
            ),
            unsafe_allow_html=True
        )

        # ----------------------------------------------
        # Extract source filenames from RAG answer
        # ----------------------------------------------
        source_files = []

        for line in answer.splitlines():

            line = line.strip()

            if line.startswith("* `") and line.endswith("`"):

                filename = line[3:-1]

                if filename not in source_files:
                    source_files.append(filename)

        # ----------------------------------------------
        # Display retrieved sources
        # ----------------------------------------------
        if source_files:

            for index, filename in enumerate(source_files):

                source_data = {
                    "id": f"rag_source_{index}",
                    "badge": "Archive",
                    "type": "report",
                    "date": "",
                    "title": filename,
                    "excerpt": (
                        "Source document retrieved from the "
                        "NewsVault AI archive."
                    ),
                    "relevance": ""
                }

                if render_source_card(
                    source_data["id"],
                    source_data["badge"],
                    source_data["type"],
                    source_data["date"],
                    source_data["title"]
                ):
                    st.session_state["selected_evidence"] = source_data
                    st.rerun()

        else:

            st.info(
                "No source documents were identified."
            )

    # ==================================================
    # Evidence Modal
    # ==================================================
    selected = st.session_state.get(
        "selected_evidence"
    )

    if selected:

        render_evidence_modal(
            source_title=selected["title"],
            badge_label=selected["badge"],
            date_str=selected["date"],
            excerpt=selected["excerpt"],
            relevance=selected["relevance"]
        )

    # --------------------------------------------------
    # Close wrapper
    # --------------------------------------------------
    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )