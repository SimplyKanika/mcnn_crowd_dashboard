"""
============================================================
About Page Component — pages/about.py
============================================================
Renders project research specifications, team details,
academic contexts, guides, reference lists, and contact
information in premium glassmorphism layouts.
============================================================
"""

import streamlit as st
from utils.dummy_data import (
    PROJECT_INFO,
    PROBLEM_STATEMENT,
    METHODOLOGY,
    EXPECTED_OUTCOMES,
    FUTURE_SCOPE,
    PROJECT_FEATURES,
    TEAM_MEMBERS,
    GUIDE_INFO,
    REFERENCES,
    ACKNOWLEDGEMENTS,
)
from components.navbar import render_page_header
from components.cards import (
    render_team_card,
    render_section_separator,
)


def render_about_page():
    """Render the About Page content."""
    render_page_header(
        title="Project Specifications & Team",
        subtitle="Academic context, project statement, methodology details, references, and team members.",
        badge_text="About Project",
    )

    # ── Section 1: Academic Affiliation Info ──
    st.markdown(
        f"""
        <div class="glass-card animate-fade-in-up" style="margin-bottom: 2rem; border-color: var(--primary-600); text-align: center;">
            <span class="hero-badge">Academic Credentials</span>
            <h2 class="gradient-text" style="margin: 0.5rem 0;">{PROJECT_INFO['title']}</h2>
            <h3 style="color: var(--text-primary); font-size: 1.25rem !important; font-weight: 500; margin-bottom: 1rem;">
                {PROJECT_INFO['subtitle']}
            </h3>
            <p style="font-size: 0.9rem; color: var(--text-secondary); margin: 0;">
                A Project submitted in partial fulfillment of the requirements for the degree of 
                <strong>Bachelor of Engineering in {PROJECT_INFO['department']}</strong>
            </p>
            <div style="font-size: 0.82rem; color: var(--text-tertiary); margin-top: 0.8rem; display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap;">
                <span>🏫 <strong>Affiliation:</strong> {PROJECT_INFO['institution']}</span>
                <span>🎓 <strong>University:</strong> {PROJECT_INFO['university']}</span>
                <span>🗓️ <strong>Academic Year:</strong> {PROJECT_INFO['year']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Section 2: Statement & Methodology ──
    col_prob, col_meth = st.columns(2)

    with col_prob:
        st.markdown(
            f"""
            <div class="glass-card" style="height: 100%;">
                <h3 class="gradient-text" style="margin-bottom: 1rem;">⚠️ Problem Statement</h3>
                <p style="line-height: 1.7; font-size: 0.9rem;">{PROBLEM_STATEMENT}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_meth:
        st.markdown(
            f"""
            <div class="glass-card" style="height: 100%;">
                <h3 class="gradient-text" style="margin-bottom: 1rem;">⚙️ Methodology</h3>
                <p style="line-height: 1.7; font-size: 0.9rem;">{METHODOLOGY}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_section_separator()

    # ── Section 3: Project Features Grid ──
    st.markdown(
        """
        <div class="section-header">
            <span class="section-badge">Dashboard Details</span>
            <h2 class="section-title">Built-in Features</h2>
            <p class="section-subtitle">A summary of the frontend dashboard features provided in this prototype.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
    for i, feat in enumerate(PROJECT_FEATURES):
        current_col = [feat_col1, feat_col2, feat_col3, feat_col4][i % 4]
        with current_col:
            st.markdown(
                f"""
                <div class="glass-card-sm" style="margin-bottom: 1rem; text-align: center; height: calc(100% - 1rem);">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{feat['icon']}</div>
                    <div style="font-weight: 600; font-size: 0.9rem; color: var(--text-primary);">{feat['title']}</div>
                    <div style="font-size: 0.78rem; color: var(--text-tertiary); margin-top: 0.3rem;">{feat['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    render_section_separator()

    # ── Section 4: Expected Outcomes & Scope ──
    col_outcomes, col_scope = st.columns(2)

    with col_outcomes:
        st.markdown("<h3 style='margin-bottom: 1rem;'>🎯 Expected Outcomes</h3>", unsafe_allow_html=True)
        outcomes_html = ""
        for out in EXPECTED_OUTCOMES:
            outcomes_html += f"""
            <div style="display: flex; gap: 0.6rem; align-items: start; margin-bottom: 0.8rem;">
                <span style="color: var(--accent-emerald); font-weight: bold;">✔</span>
                <span style="font-size: 0.9rem; color: var(--text-secondary);">{out}</span>
            </div>
            """
        st.markdown(f'<div class="glass-card" style="height: calc(100% - 1rem);">{outcomes_html}</div>', unsafe_allow_html=True)

    with col_scope:
        st.markdown("<h3 style='margin-bottom: 1rem;'>🚀 Future Scope</h3>", unsafe_allow_html=True)
        scope_html = ""
        for sc in FUTURE_SCOPE:
            scope_html += f"""
            <div style="display: flex; gap: 0.6rem; align-items: start; margin-bottom: 0.8rem;">
                <span style="color: var(--primary-400); font-weight: bold;">➔</span>
                <span style="font-size: 0.9rem; color: var(--text-secondary);">{sc}</span>
            </div>
            """
        st.markdown(f'<div class="glass-card" style="height: calc(100% - 1rem);">{scope_html}</div>', unsafe_allow_html=True)

    render_section_separator()

    # ── Section 5: Team Members & Guide ──
    st.markdown(
        """
        <div class="section-header">
            <span class="section-badge">Contributors</span>
            <h2 class="section-title">The Project Team</h2>
            <p class="section-subtitle">Dedicated researchers and student developers working on this system.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Render Team Cards side by side
    team_cols = st.columns(3)
    for i, member in enumerate(TEAM_MEMBERS):
        with team_cols[i]:
            render_team_card(
                avatar=member["avatar"],
                name=member["name"],
                role=member["role"],
                bio=member["bio"],
            )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Guide Card (Full-width / Centered)
    col_g1, col_g2, col_g3 = st.columns([1, 1.2, 1])
    with col_g2:
        st.markdown(
            f"""
            <div class="team-card animate-pulse-glow" style="border-color: var(--primary-600);">
                <div class="team-avatar" style="background: var(--gradient-primary);">{GUIDE_INFO['avatar']}</div>
                <div class="team-name">{GUIDE_INFO['name']}</div>
                <div class="team-role" style="color: var(--primary-300);">{GUIDE_INFO['role']}</div>
                <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.2rem;">{GUIDE_INFO['department']}</div>
                <div class="team-bio" style="font-size: 0.82rem; color: var(--text-tertiary); margin-top: 0.6rem;">
                    Providing essential technical directions, architecture review guidance, and academic supervision for this project.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_section_separator()

    # ── Section 6: Acknowledgements & References ──
    col_ack, col_ref = st.columns([1, 1])

    with col_ack:
        st.markdown("<h3 style='margin-bottom: 1rem;'>🙏 Acknowledgements</h3>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="glass-card" style="height: calc(100% - 1rem);">
                <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.7; margin: 0;">
                    {ACKNOWLEDGEMENTS}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_ref:
        st.markdown("<h3 style='margin-bottom: 1rem;'>📚 References</h3>", unsafe_allow_html=True)
        refs_html = ""
        for i, ref in enumerate(REFERENCES):
            refs_html += f"""
            <div style="display: flex; gap: 0.6rem; align-items: start; margin-bottom: 0.8rem; font-size: 0.85rem;">
                <span style="color: var(--primary-300); font-family: monospace;">[{i+1}]</span>
                <span style="color: var(--text-secondary); line-height: 1.5;">{ref}</span>
            </div>
            """
        st.markdown(f'<div class="glass-card" style="height: calc(100% - 1rem);">{refs_html}</div>', unsafe_allow_html=True)

    render_section_separator()

    # ── Section 7: Contact Section ──
    st.markdown(
        """
        <div class="glass-card text-center animate-fade-in-up" style="padding: 2.5rem 1.5rem; background: var(--bg-hover);">
            <h3 class="gradient-text">Get in Touch</h3>
            <p style="max-width: 500px; margin: 0.5rem auto 1.5rem auto; font-size: 0.88rem; color: var(--text-secondary);">
                For collaboration, feedback, or technical queries regarding the Enhanced MCNN framework, feel free to reach out.
            </p>
            <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; font-size: 0.85rem; color: var(--text-tertiary);">
                <span>📧 <strong>Email:</strong> project.mcnn@xyzcollege.edu</span>
                <span>🌐 <strong>GitHub:</strong> github.com/mcnn-crowd-density</span>
                <span>📍 <strong>Location:</strong> Mumbai, India</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
