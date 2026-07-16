"""
============================================================
Cards Component — Reusable Card UI Elements
============================================================
Provides functions to render various card types:
metric, feature, info, tech, team, architecture, and result cards.
All use glassmorphism styling from style.css.
============================================================
"""

import streamlit as st


def render_metric_card(icon, value, label, color="purple"):
    """
    Render a single metric/stat card with icon, value, and label.

    Args:
        icon: Emoji or icon string.
        value: Display value (e.g., '95.6%').
        label: Label text below the value.
        color: Color variant (purple, blue, emerald, amber, rose, cyan).
    """
    st.markdown(
        f"""
        <div class="metric-card {color}">
            <span class="metric-icon">{icon}</span>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_card(icon, title, desc):
    """
    Render a feature card with icon, title, and description.

    Args:
        icon: Emoji icon.
        title: Feature title.
        desc: Feature description.
    """
    st.markdown(
        f"""
        <div class="feature-card">
            <span class="feature-icon">{icon}</span>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_card(icon, title, content):
    """
    Render an information card for text-heavy content.

    Args:
        icon: Emoji icon.
        title: Card heading.
        content: Main text content (HTML or plain text).
    """
    st.markdown(
        f"""
        <div class="info-card">
            <h4>{icon} {title}</h4>
            <p>{content}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_tech_card(icon, name, desc):
    """
    Render a compact technology stack card.

    Args:
        icon: Emoji icon.
        name: Technology name.
        desc: Short description.
    """
    st.markdown(
        f"""
        <div class="tech-card">
            <span class="tech-icon">{icon}</span>
            <div class="tech-name">{name}</div>
            <div class="tech-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_team_card(avatar, name, role, bio):
    """
    Render a team member card with avatar, name, role, and bio.

    Args:
        avatar: Emoji avatar.
        name: Team member name.
        role: Role/title.
        bio: Short biography.
    """
    st.markdown(
        f"""
        <div class="team-card">
            <div class="team-avatar">{avatar}</div>
            <div class="team-name">{name}</div>
            <div class="team-role">{role}</div>
            <div class="team-bio">{bio}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_arch_card(icon, title, description):
    """
    Render an architecture/diagram explanation card.

    Args:
        icon: Emoji icon.
        title: Architecture component title.
        description: Detailed explanation.
    """
    st.markdown(
        f"""
        <div class="arch-card">
            <div class="arch-title">{icon} {title}</div>
            <div class="arch-desc">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_cnn_column_card(icon, name, filter_size, description, layers):
    """
    Render a CNN column visualization card.

    Args:
        icon: Emoji icon.
        name: Column name (e.g., 'Column A — Fine Scale').
        filter_size: Filter size string (e.g., '3×3 Conv').
        description: What this column captures.
        layers: Layer architecture string.
    """
    st.markdown(
        f"""
        <div class="cnn-column">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <div class="column-name">{name}</div>
            <div class="filter-info">{filter_size}</div>
            <p style="font-size: 0.8rem; color: #94A3B8; margin-top: 0.8rem;
                      line-height: 1.6;">{description}</p>
            <div style="margin-top: 0.6rem; padding: 0.5rem; background: rgba(15,15,26,0.5);
                        border-radius: 0.5rem;">
                <code style="font-size: 0.7rem;">{layers}</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result_card(value, label, icon=""):
    """
    Render a prediction result card with large value.

    Args:
        value: The result value to display.
        label: Label for the value.
        icon: Optional emoji icon.
    """
    icon_html = f'<span style="font-size: 1.5rem;">{icon}</span>' if icon else ""
    st.markdown(
        f"""
        <div class="result-card" style="text-align: center;">
            {icon_html}
            <div class="result-value">{value}</div>
            <div class="result-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_glass_card(content_html):
    """
    Render a generic glassmorphism card with custom HTML content.

    Args:
        content_html: Raw HTML to place inside the card.
    """
    st.markdown(
        f"""
        <div class="glass-card">
            {content_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_timeline(steps):
    """
    Render a workflow timeline from a list of step dicts.

    Args:
        steps: List of dicts with 'step', 'title', 'desc' keys.
    """
    timeline_html = '<div class="timeline">'
    for i, step in enumerate(steps):
        active_class = "active" if i == len(steps) - 1 else ""
        timeline_html += f"""
            <div class="timeline-item">
                <div class="timeline-dot {active_class}"></div>
                <div class="timeline-content">
                    <div class="timeline-title">
                        Step {step['step']}: {step['title']}
                    </div>
                    <div class="timeline-desc">{step['desc']}</div>
                </div>
            </div>
        """
    timeline_html += "</div>"
    st.markdown(timeline_html, unsafe_allow_html=True)


def render_badge(text, badge_type="purple"):
    """
    Render a small status badge.

    Args:
        text: Badge text.
        badge_type: One of 'success', 'warning', 'danger', 'info', 'purple'.
    """
    st.markdown(
        f'<span class="badge badge-{badge_type}">{text}</span>',
        unsafe_allow_html=True,
    )


def render_density_badge(level, css_class):
    """
    Render a density level badge (Low, Medium, High, Very High).

    Args:
        level: Density level text.
        css_class: CSS class name (density-low, density-medium, etc.).
    """
    st.markdown(
        f'<span class="{css_class}">{level}</span>',
        unsafe_allow_html=True,
    )


def render_gradient_divider():
    """Render a gradient horizontal divider."""
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)


def render_section_separator():
    """Render a subtle section separator."""
    st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
