import streamlit as st


def clean_html(html_str: str) -> str:
    return " ".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_source_card(source_id: str, badge_label: str, badge_icon_type: str, date_str: str, title: str):
    """
    Renders a single primary source card matching the Figma design.
    Returns True if the 'View Evidence' button was clicked.
    """
    # SVG icons for badge types
    if badge_icon_type == "article":
        icon_svg = """<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>"""
    elif badge_icon_type == "interview":
        icon_svg = """<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>"""
    else:  # report or document
        icon_svg = """<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="12" y1="18" x2="12" y2="12"></line><line x1="9" y1="15" x2="12" y2="12"></line><line x1="15" y1="15" x2="12" y2="12"></line></svg>"""

    card_top_html = clean_html(f"""
    <div class="source-card-wrapper">
        <div class="source-card-header">
            <div class="source-badge">
                <span class="source-badge-icon">{icon_svg}</span>
                <span>{badge_label}</span>
            </div>
            <span class="source-date">{date_str}</span>
        </div>
        <h4 class="source-title">{title}</h4>
    </div>
    """)
    st.markdown(card_top_html, unsafe_allow_html=True)

    clicked = st.button(
        "👁 View Evidence",
        key=f"btn_evidence_{source_id}",
        use_container_width=True
    )
    return clicked
