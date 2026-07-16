
import streamlit as st

print("Loaded footer from:", __file__)

def render_footer():
    """Render the professional footer at the bottom of each page."""
    st.markdown(
        """
        <div class="custom-footer">
            <div class="footer-brand">CrowdVision AI</div>
            <p style="font-size: 0.82rem; color: #64748B; margin-bottom: 0.8rem;">
                Enhanced MCNN for Accurate Crowd Density Estimation
            </p>
            <div class="footer-divider"></div>
            <div class="footer-links">
                <span class="footer-link"> Home</span>
                <span class="footer-link"> Prediction</span>
                <span class="footer-link"> Analytics</span>
                <span class="footer-link"> Architecture</span>
                <span class="footer-link"> About</span>
            </div>
            <div class="footer-divider"></div>
            <p class="footer-text">
                Department of Artificial Intelligence and Data Science<br>
                
                <span style="margin-top: 0.3rem; display: inline-block;">
                    © 2026 CrowdVision AI — All Rights Reserved
                </span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_mini_footer():
    """Render a compact footer for pages that need minimal footprint."""
    st.markdown(
        """
        <div style="text-align: center; padding: 1.5rem 0; margin-top: 2rem;
                    border-top: 1px solid rgba(255,255,255,0.06);">
            <p style="font-size: 0.75rem; color: #475569;">
                © 2026 CrowdVision AI · Enhanced MCNN Dashboard v2.1.0
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
