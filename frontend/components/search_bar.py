import streamlit as st


def clean_html(html_str: str) -> str:
    return " ".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_search_bar():
    if "archive_question" not in st.session_state:
        st.session_state["archive_question"] = ""

    with st.container():
        st.markdown(clean_html('<div class="question-label">ASK A QUESTION ABOUT THE ARCHIVE:</div>'), unsafe_allow_html=True)

        col1, col2 = st.columns([4.8, 1.2], gap="small")

        with col1:
            question = st.text_input(
                "Archive question",
                value=st.session_state.get("archive_question", ""),
                placeholder="What did we report about X in 2018?",
                label_visibility="collapsed",
                key="archive_question_input"
            )

        with col2:
            search_clicked = st.button(
                "▷ Search",
                use_container_width=True,
                key="search_button"
            )

        st.markdown(clean_html('<div class="examples-title">TRY EXAMPLE QUESTIONS:</div>'), unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1.1, 1.1, 1.0])
        chip_clicked = False

        with c1:
            if st.button("💡 What were the main headlines in 2019?", key="chip_1"):
                question = "What were the main headlines in 2019?"
                st.session_state["archive_question"] = question
                chip_clicked = True

        with c2:
            if st.button("💡 Find reports about climate change", key="chip_2"):
                question = "Find reports about climate change"
                st.session_state["archive_question"] = question
                chip_clicked = True

        with c3:
            if st.button("💡 Interviews with the CEO in 2020", key="chip_3"):
                question = "Interviews with the CEO in 2020"
                st.session_state["archive_question"] = question
                chip_clicked = True

    return question, (search_clicked or chip_clicked)