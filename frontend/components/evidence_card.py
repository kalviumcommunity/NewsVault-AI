import html
import streamlit as st


def render_evidence_modal(
    source_title: str,
    badge_label: str,
    date_str: str,
    excerpt: str,
    relevance: str = "96%"
):
    """
    Renders the evidence view showing the actual
    retrieved archive chunk.
    """

    if not date_str:
        date_str = "Archive"

    if not relevance:
        relevance = "Match"

    if not excerpt or not excerpt.strip():
        excerpt = "No excerpt available."

    # Escape dynamic text so document content cannot break the HTML.
    safe_title = html.escape(str(source_title))
    safe_badge = html.escape(str(badge_label))
    safe_date = html.escape(str(date_str))
    safe_relevance = html.escape(str(relevance))
    safe_excerpt = html.escape(str(excerpt))

    evidence_html = f"""
    <div class="evidence-modal-backdrop">

        <div class="evidence-modal-card">

            <div class="evidence-modal-header">

                <div>
                    <span class="evidence-modal-badge">
                        {safe_badge}
                    </span>

                    <span class="evidence-modal-date">
                        • {safe_date}
                    </span>
                </div>

                <div class="evidence-relevance-pill">
                    Match: {safe_relevance}
                </div>

            </div>

            <h3 class="evidence-modal-title">
                {safe_title}
            </h3>

            <div class="evidence-modal-body">

                <div class="evidence-quote-label">
                    EXCERPT EVIDENCE:
                </div>

                <blockquote class="evidence-quote-box">
                    "{safe_excerpt}"
                </blockquote>

            </div>

        </div>

    </div>
    """

    # Render HTML directly instead of using st.markdown.
    st.html(evidence_html)

    if st.button(
        "✕ Close Evidence View",
        key="close_evidence_btn",
        use_container_width=True
    ):
        st.session_state["selected_evidence"] = None
        st.rerun()