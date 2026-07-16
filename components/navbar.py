"""
============================================================
Navbar Component — Top Navigation Bar
============================================================
Renders a premium top bar with brand, status indicator,
and model version info.
============================================================
"""

import streamlit as st


def render_navbar():
    """Render the top navigation bar with brand and status."""
    st.markdown(
        """
        <div class="navbar">
            <div class="navbar-brand">
                <div>
                    <span class="navbar-title">CrowdVision AI</span>
                    <span style="font-size: 0.7rem; color: #64748B; margin-left: 0.5rem;">
                        Enhanced MCNN Dashboard
                    </span>
                </div>
            </div>
            <div class="navbar-status">
                <span class="status-dot online"></span>
                Model Online — v2.1.0
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title, subtitle="", badge_text=""):
    """
    Render a page-level header with optional badge and subtitle.

    Args:
        title: Main page title.
        subtitle: Optional description below the title.
        badge_text: Optional small badge above the title.
    """
    badge_html = ""
    if badge_text:
        badge_html = f'<span class="section-badge">{badge_text}</span><br>'

    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<p class="section-subtitle">{subtitle}</p>'

    st.markdown(
        f"""
        <div class="section-header">
            {badge_html}
            <h1 class="section-title">{title}</h1>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
