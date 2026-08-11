"""
============================================================
Footer Component — components/footer.py
============================================================
Professional 3-column footer matching the reference layout.
Uses st.columns to place Streamlit nav buttons into the
correct middle column alongside the static HTML sections.
All HTML rendered via st.markdown(unsafe_allow_html=True).
============================================================
"""

import streamlit as st
import os
import base64


_PAGES = ["Home", "Prediction", "Analytics", "Model Details", "About"]

_NAV_ICONS = {
    "Home": "🏠",
    "Prediction": "🧠",
    "Analytics": "📊",
    "Model Details": "🔬",
    "About": "ℹ️",
}


def _get_logo_b64() -> str:
    """Return base64-encoded logo or empty string."""
    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png"
    )
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as fh:
            return base64.b64encode(fh.read()).decode()
    return ""


def render_footer() -> None:
    """
    Render the unified 3-column glassmorphism footer on every page.

    Layout
    ------
    Uses st.columns([50, 25, 25]) so Streamlit buttons can be placed
    natively inside the middle column while static HTML is in the left
    and right columns.

    Left   (~50%) : Brand, headline, description, status badge
    Middle (~25%) : QUICK NAVIGATION — real Streamlit buttons
    Right  (~25%) : PROJECT / TECHNOLOGY list

    Bottom row    : Department info (left) | copyright (right)
    """

    logo_b64 = _get_logo_b64()
    logo_html = (
        f'<img src="data:image/png;base64,{logo_b64}" '
        f'alt="CrowdVision AI Logo" class="ft-logo-img">'
        if logo_b64
        else '<span class="ft-logo-emoji">&#129302;</span>'
    )

    # ── Outer wrapper open ─────────────────────────────────────────
    st.markdown('<div class="cv-footer">', unsafe_allow_html=True)
    st.markdown('<div class="ft-top-section">', unsafe_allow_html=True)

    # ── 3 columns (50 / 25 / 25) ──────────────────────────────────
    col_brand, col_nav, col_tech = st.columns([50, 25, 25])

    # LEFT — Brand
    with col_brand:
        st.markdown(
            f"""
<div class="ft-col ft-col-brand">
  <div class="ft-brand-row">
    {logo_html}
    <span class="ft-brand-name">CrowdVision AI</span>
  </div>
  <p class="ft-headline">
    Enhanced Multi-Column CNN for Accurate Crowd Density Estimation
  </p>
  <p class="ft-desc">
    AI-powered crowd density estimation using Enhanced MCNN and
    Adaptive Collation for pixel-level density mapping and real-time
    crowd count analytics.
  </p>
  <div class="ft-status-badge">
    <span class="status-dot online"></span>
    <span class="ft-status-txt">Model Engine Online&nbsp;&bull;&nbsp;v2.1.0</span>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    # MIDDLE — Quick Navigation
    with col_nav:
        st.markdown(
            '<div class="ft-col ft-col-nav">',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<h6 class="ft-col-heading">QUICK NAVIGATION</h6>',
            unsafe_allow_html=True,
        )
        # Functional Streamlit buttons styled as text links via CSS
        for page in _PAGES:
            icon = _NAV_ICONS[page]
            if st.button(
                f"{icon} {page}",
                key=f"ft_nav_{page}",
                use_container_width=True,
            ):
                st.session_state["_footer_nav_target"] = page
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # RIGHT — Project / Technology
    with col_tech:
        st.markdown(
            """
<div class="ft-col ft-col-tech">
  <h6 class="ft-col-heading">PROJECT</h6>
  <ul class="ft-link-list">
    <li><span class="ft-bullet">&#9670;</span>Enhanced MCNN</li>
    <li><span class="ft-bullet">&#9670;</span>Crowd Density Estimation</li>
    <li><span class="ft-bullet">&#9670;</span>Adaptive Collation</li>
    <li><span class="ft-bullet">&#9670;</span>PyTorch</li>
    <li><span class="ft-bullet">&#9670;</span>Streamlit Dashboard</li>
  </ul>
</div>
""",
            unsafe_allow_html=True,
        )

    # ── Close top section, add divider + bottom row ────────────────
    st.markdown("</div>", unsafe_allow_html=True)   # /.ft-top-section

    st.markdown(
        """
<div class="ft-divider"></div>
<div class="ft-bottom">
  <div class="ft-bottom-left">
    <span>Department of Artificial Intelligence &amp; Data Science</span>
    <span class="ft-bottom-sep">|</span>
    <span>Enhanced MCNN Crowd Density Estimation Project</span>
  </div>
  <div class="ft-bottom-right">
    <span>&copy; 2026 <strong>CrowdVision AI</strong></span>
    <span class="ft-bottom-sep">|</span>
    <span>All Rights Reserved</span>
  </div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_mini_footer() -> None:
    """Alias — keeps the same footer everywhere."""
    render_footer()
