"""
============================================================
Enhanced MCNN Crowd Density Dashboard — Main Application
============================================================
Entry point for the Streamlit application.
Configures the page, loads global CSS, renders sidebar
navigation, routes to the selected page, and displays
the footer.

Run with:  streamlit run app.py
============================================================
"""

import streamlit as st
import os

# ── Page Configuration (must be first Streamlit call) ──
st.set_page_config(
    page_title="CrowdVision AI — Enhanced MCNN Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Enhanced MCNN Crowd Density Estimation Dashboard v2.1.0",
    },
)


# ============================================================
# CSS LOADER
# ============================================================

def load_css():
    """Load the global custom CSS stylesheet."""
    css_path = os.path.join(
        os.path.dirname(__file__), "styles", "style.css"
    )
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    """Main application entry point."""

    # 1. Load global styles
    load_css()

    # 2. Render sidebar and get selected page
    from components.sidebar import render_sidebar
    selected_page = render_sidebar()

    # 3. Render top navbar
    from components.navbar import render_navbar
    render_navbar()

    # 4. Route to the selected page
    if selected_page == "Home":
        from pages.home import render_home_page
        render_home_page()

    elif selected_page == "Prediction":
        from pages.prediction import render_prediction_page
        render_prediction_page()

    elif selected_page == "Analytics":
        from pages.analytics import render_analytics_page
        render_analytics_page()

    elif selected_page == "Model Details":
        from pages.model_details import render_model_details_page
        render_model_details_page()

    elif selected_page == "About":
        from pages.about import render_about_page
        render_about_page()

    # 5. Render footer
    from components.footer import render_footer
    render_footer()


# ── Entry Point ──
if __name__ == "__main__":
    main()
