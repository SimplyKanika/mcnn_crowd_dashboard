"""
============================================================
Home Page Component — pages/home.py
============================================================
Renders the premium hero landing page for the project.
Includes details of objectives, technology stack, features,
workflow timeline, statistic cards, and action buttons.
============================================================
"""

import streamlit as st
import os
import base64
from utils.dummy_data import (
    PROJECT_INFO,
    PROJECT_OVERVIEW,
    RESEARCH_MOTIVATION,
    HERO_STATS,
    OBJECTIVES,
    TECH_STACK,
    FEATURES,
    WORKFLOW_STEPS,
)
from components.navbar import render_page_header
from components.cards import (
    render_metric_card,
    render_feature_card,
    render_tech_card,
    render_timeline,
)


def get_image_base64(image_path):
    """Convert an image file to base64 string for HTML embedding."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def render_home_page():
    """Render the Home Page content."""
    # ── Page Title / Header ──
    render_page_header(
        title="Crowd Density Estimation System",
        subtitle="Enhanced Multi-Column Convolutional Neural Network with Adaptive Collation",
        badge_text="AI Prototype Project",
    )

    # ── Hero Banner Section ──
    hero_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "assets", "hero_banner.png"
    )
    hero_b64 = get_image_base64(hero_path)

    # Glassmorphism container for hero
    st.markdown(
        f"""
        <div class="hero-section animate-fade-in-up">
            <span class="hero-badge">Deep Learning Core</span>
            <h1 class="hero-title">
                <span class="gradient-text">Enhanced MCNN Architecture</span>
            </h1>
            <p class="hero-subtitle">
                Capturing multi-scale crowd features dynamically through parallel convolutional pipelines 
                and adaptive attention-based collation for pixel-level crowd density mapping.
            </p>
            <div class="hero-image">
                <img src="data:image/png;base64,{hero_b64}" alt="AI Crowd Vision Hero Banner">
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Animated Stat Cards Section ──
    st.markdown("<div style='margin: 2rem 0 1rem 0; text-align: center;'><h3>System Highlights</h3></div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    for i, col in enumerate([col1, col2, col3, col4]):
        stat = HERO_STATS[i]
        with col:
            render_metric_card(
                icon=stat["icon"],
                value=stat["value"],
                label=stat["label"],
                color=stat["color"],
            )

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # ── Overview and Motivation (Side by Side) ──
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown(
            f"""
            <div class="glass-card animate-fade-in-up delay-100" style="height: 100%;">
                <h3 class="gradient-text">Project Overview</h3>
                <p style="margin-top: 1rem;">{PROJECT_OVERVIEW}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            f"""
            <div class="glass-card animate-fade-in-up delay-200" style="height: 100%;">
                <h3 class="gradient-text">Research Motivation</h3>
                <p style="margin-top: 1rem;">{RESEARCH_MOTIVATION}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # ── Project Objectives ──
    st.markdown(
        """
        <div class="section-header">
            <span class="section-badge">Goals</span>
            <h2 class="section-title">Key Objectives</h2>
            <p class="section-subtitle">What we aim to achieve with the Enhanced MCNN framework</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    obj_col1, obj_col2, obj_col3 = st.columns(3)
    for i, obj in enumerate(OBJECTIVES):
        current_col = [obj_col1, obj_col2, obj_col3][i % 3]
        with current_col:
            st.markdown(
                f"""
                <div class="glass-card-sm" style="margin-bottom: 1rem; height: calc(100% - 1rem);">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{obj['icon']}</div>
                    <h4 style="color: var(--text-primary); margin-bottom: 0.5rem;">{obj['title']}</h4>
                    <p style="font-size: 0.85rem; color: var(--text-tertiary); line-height: 1.5;">{obj['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # ── Key Features Grid ──
    st.markdown(
        """
        <div class="section-header">
            <span class="section-badge">Capabilities</span>
            <h2 class="section-title">System Features</h2>
            <p class="section-subtitle">Core functionalities integrated into the CrowdVision platform</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    feat_col1, feat_col2, feat_col3 = st.columns(3)
    for i, feat in enumerate(FEATURES):
        current_col = [feat_col1, feat_col2, feat_col3][i % 3]
        with current_col:
            render_feature_card(feat["icon"], feat["title"], feat["desc"])

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # ── Workflow Timeline & Tech Stack (Side by Side) ──
    col_flow, col_tech = st.columns([3, 2])
    with col_flow:
        st.markdown(
            """
            <div class="glass-card" style="height: 100%;">
                <h3 class="gradient-text" style="margin-bottom: 1rem;">Model Execution Workflow</h3>
                <p style="font-size: 0.85rem; color: var(--text-tertiary); margin-bottom: 1.5rem;">
                    Step-by-step pipeline from crowd image input to analytics delivery.
                </p>
            """,
            unsafe_allow_html=True,
        )
        render_timeline(WORKFLOW_STEPS)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_tech:
        st.markdown(
            """
            <div class="glass-card" style="height: 100%;">
                <h3 class="gradient-text" style="margin-bottom: 1.5rem;">Technology Stack</h3>
            """,
            unsafe_allow_html=True,
        )
        tech_col1, tech_col2 = st.columns(2)
        for i, tech in enumerate(TECH_STACK):
            current_col = tech_col1 if i % 2 == 0 else tech_col2
            with current_col:
                render_tech_card(tech["icon"], tech["name"], tech["desc"])
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # ── CTA Actions Section ──
    st.markdown(
        """
        <div class="glass-card text-center animate-pulse-glow" style="padding: 3rem 2rem;">
            <h2 class="gradient-text">Estimate Crowd Density Now</h2>
            <p style="max-width: 600px; margin: 1rem auto 2rem auto;">
                Experience the Enhanced MCNN pipeline. Upload a crowd image to view estimated density mapping, 
                intensity heatmaps, and precise head counts instantly.
            </p>
            <div style="display: inline-flex; gap: 1.5rem; justify-content: center; align-items: center; width: 100%; flex-wrap: wrap;">
                <div class="btn-primary" style="cursor: default;">
                    🚀 Start Prediction (Use Sidebar)
                </div>
                <div class="btn-secondary" style="cursor: default;">
                    📚 Learn More
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
