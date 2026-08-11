"""
============================================================
Sidebar Component — Icon-based Navigation
============================================================
Renders the sidebar with logo, navigation menu using
streamlit-option-menu, and version info.
============================================================
"""

import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64


def get_image_base64(image_path):
    """Convert an image file to base64 string for HTML embedding."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def render_sidebar():
    """
    Render the sidebar with logo, navigation, and footer info.
    Returns the selected page name as a string.
    """
    with st.sidebar:
        # ── Logo & Brand ──
        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png"
        )
        logo_b64 = get_image_base64(logo_path)

        st.markdown(
            f"""
            <div class="sidebar-logo">
                <img src="data:image/png;base64,{logo_b64}" alt="Logo">
                <h3>CrowdVision AI</h3>
                <p>Enhanced MCNN Dashboard</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Compute default index — respect footer nav overrides
        _pages = ["Home", "Prediction", "Analytics", "Model Details", "About"]
        _nav_target = st.session_state.get("_footer_nav_target", None)
        _default_idx = _pages.index(_nav_target) if _nav_target in _pages else 0

        selected = option_menu(
            menu_title=None,
            options=_pages,
            icons=[
                "house-fill",
                "cpu-fill",
                "bar-chart-fill",
                "diagram-3-fill",
                "info-circle-fill",
            ],
            default_index=_default_idx,
            styles={
                "container": {
                    "padding": "0.5rem 0",
                    "background-color": "transparent",
                },
                "icon": {
                    "color": "#A78BFA",
                    "font-size": "1rem",
                },
                "nav-link": {
                    "font-family": "'Inter', sans-serif",
                    "font-size": "0.9rem",
                    "font-weight": "500",
                    "color": "#94A3B8",
                    "border-radius": "0.75rem",
                    "padding": "0.65rem 1rem",
                    "margin": "0.15rem 0.5rem",
                    "transition": "all 0.3s ease",
                },
                "nav-link:hover": {
                    "background-color": "rgba(124, 58, 237, 0.08)",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #7C3AED, #3B82F6)",
                    "color": "white",
                    "font-weight": "600",
                    "box-shadow": "0 0 15px rgba(124, 58, 237, 0.3)",
                },
            },
        )

        # ── Sidebar Footer ──
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; padding: 0.5rem;">
                <span class="version-tag">v2.1.0</span>
                <p style="font-size: 0.7rem; color: #475569; margin-top: 0.5rem;">
                    © CrowdVision AI
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected
