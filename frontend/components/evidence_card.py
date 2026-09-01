import streamlit as st


def clean_html(html_str: str) -> str:
    return " ".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_evidence_modal(source_title: str, badge_label: str, date_str: str, excerpt: str, relevance: str = "96%"):
    """
    Renders an evidence drawer modal when a source card's 'View Evidence' button is clicked.
    """
    st.markdown(clean_html(f"""
    <div class="evidence-modal-backdrop">
        <div class="evidence-modal-card">
            <div class="evidence-modal-header">
                <div>
                    <span class="evidence-modal-badge">{badge_label}</span>
                    <span class="evidence-modal-date">• {date_str}</span>
                </div>
                <div class="evidence-relevance-pill">Match: {relevance}</div>
            </div>
            <h3 class="evidence-modal-title">{source_title}</h3>
            <div class="evidence-modal-body">
                <div class="evidence-quote-label">EXCERPT EVIDENCE:</div>
                <blockquote class="evidence-quote-box">"{excerpt}"</blockquote>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    if st.button("✕ Close Evidence View", key="close_evidence_btn", use_container_width=True):
        st.session_state["selected_evidence"] = None
        st.rerun()
