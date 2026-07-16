"""
============================================================
Buttons Component — Custom Styled Buttons
============================================================
Provides functions to render gradient and styled buttons
using HTML/CSS. These are visual-only; for functional buttons,
use Streamlit's native st.button with CSS overrides.
============================================================
"""

import streamlit as st


def render_primary_button(text, icon="", key=None):
    """
    Render a gradient primary CTA button via HTML.
    Note: This is display-only. Use st.button for interactivity.

    Args:
        text: Button label.
        icon: Optional emoji icon.
        key: Unused, for API consistency.
    """
    st.markdown(
        f"""
        <div style="text-align: center; margin: 0.5rem 0;">
            <span class="btn-primary">{icon} {text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_secondary_button(text, icon=""):
    """
    Render a bordered secondary button via HTML.

    Args:
        text: Button label.
        icon: Optional emoji icon.
    """
    st.markdown(
        f"""
        <div style="text-align: center; margin: 0.5rem 0;">
            <span class="btn-secondary">{icon} {text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_accent_button(text, icon=""):
    """
    Render a multi-color gradient accent button via HTML.

    Args:
        text: Button label.
        icon: Optional emoji icon.
    """
    st.markdown(
        f"""
        <div style="text-align: center; margin: 0.5rem 0;">
            <span class="btn-accent">{icon} {text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_button_row(buttons):
    """
    Render a row of buttons side by side.

    Args:
        buttons: List of dicts with 'text', 'icon', and 'type'
                 (primary/secondary/accent) keys.
    """
    cols = st.columns(len(buttons))
    for col, btn in zip(cols, buttons):
        with col:
            btn_type = btn.get("type", "primary")
            icon = btn.get("icon", "")
            text = btn.get("text", "Button")
            if btn_type == "primary":
                render_primary_button(text, icon)
            elif btn_type == "secondary":
                render_secondary_button(text, icon)
            else:
                render_accent_button(text, icon)
