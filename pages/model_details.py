"""
============================================================
Model Details Page Component — pages/model_details.py
============================================================
Renders the architectural specifications and details.
Illustrates the Enhanced MCNN columns, Adaptive Collation
fusion method, density map integration, applications,
and future improvements.
============================================================
"""

import streamlit as st
from utils.dummy_data import (
    MCNN_ARCHITECTURE,
    ADVANTAGES,
    APPLICATIONS,
    FUTURE_IMPROVEMENTS,
)
from components.navbar import render_page_header
from components.cards import (
    render_arch_card,
    render_cnn_column_card,
    render_feature_card,
    render_section_separator,
)


def render_model_details_page():
    """Render the Model Details Page content."""
    render_page_header(
        title="Enhanced MCNN Architecture",
        subtitle="Technical overview and deep learning specifications of the Multi-Column CNN with Adaptive Collation.",
        badge_text="Model Blueprint",
    )

    # ── Section 1: Architecture Concept ──
    st.markdown(
        """
        <div class="glass-card animate-fade-in-up" style="margin-bottom: 2rem;">
            <h3 class="gradient-text" style="margin-bottom: 1rem;">Core Concept: Scale-Aware Crowd Counting</h3>
            <p style="line-height: 1.7;">
                Crowd images exhibit massive variations in head sizes due to perspective distortion (e.g., objects near the camera 
                appear large, while those far away appear extremely small). Standard single-column CNNs fail to maintain high accuracy
                across these scales. Our <strong>Enhanced Multi-Column Convolutional Neural Network (MCNN)</strong> addresses this by using
                parallel network branches optimized for different spatial scales.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Section 2: The Three Parallel Columns ──
    st.markdown(
        """
        <div class="section-header">
            <span class="section-badge">Feature Extraction</span>
            <h2 class="section-title">Three Parallel CNN Columns</h2>
            <p class="section-subtitle">Each column processes the input in parallel using distinct kernel sizes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    columns_data = MCNN_ARCHITECTURE["columns"]

    with col1:
        render_cnn_column_card(
            icon=columns_data[0]["icon"],
            name=columns_data[0]["name"],
            filter_size=columns_data[0]["filter"],
            description=columns_data[0]["desc"],
            layers=columns_data[0]["layers"],
        )

    with col2:
        render_cnn_column_card(
            icon=columns_data[1]["icon"],
            name=columns_data[1]["name"],
            filter_size=columns_data[1]["filter"],
            description=columns_data[1]["desc"],
            layers=columns_data[1]["layers"],
        )

    with col3:
        render_cnn_column_card(
            icon=columns_data[2]["icon"],
            name=columns_data[2]["name"],
            filter_size=columns_data[2]["filter"],
            description=columns_data[2]["desc"],
            layers=columns_data[2]["layers"],
        )

    render_section_separator()

    # ── Section 3: Adaptive Collation & Density Generation ──
    col_collate, col_densmap = st.columns(2)

    with col_collate:
        render_arch_card(
            icon="🔗",
            title="Adaptive Collation Mechanism",
            description=MCNN_ARCHITECTURE["collation"]
        )

    with col_densmap:
        render_arch_card(
            icon="🗺️",
            title="Density Map Integration",
            description=MCNN_ARCHITECTURE["density_map"]
        )

    render_section_separator()

    # ── Section 4: Dataflow Pipeline Flowchart ──
    st.markdown(
        """
        <div class="section-header">
            <span class="section-badge">Data Flow</span>
            <h2 class="section-title">Model Inference Pipeline</h2>
            <p class="section-subtitle">Visual representation of data routing from input image to final crowd analytics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Reusable CSS-styled flow chart blocks for pipeline
    st.markdown(
        """
        <div class="glass-card animate-fade-in-up" style="padding: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; text-align: center;">
                <div style="flex: 1; min-width: 140px; padding: 1rem; background: rgba(15,15,26,0.6); border: 1px solid var(--border-secondary); border-radius: var(--radius-md);">
                    <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">🖼️</div>
                    <div style="font-weight: 600; font-size: 0.85rem; color: var(--text-primary);">Crowd Image Input</div>
                    <div style="font-size: 0.7rem; color: var(--text-tertiary); margin-top: 0.2rem;">Raw Capture</div>
                </div>
                <div style="font-size: 1.5rem; color: var(--primary-500);">➔</div>
                <div style="flex: 1; min-width: 140px; padding: 1rem; background: rgba(15,15,26,0.6); border: 1px solid var(--border-secondary); border-radius: var(--radius-md);">
                    <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">⚙️</div>
                    <div style="font-weight: 600; font-size: 0.85rem; color: var(--text-primary);">Preprocessing</div>
                    <div style="font-size: 0.7rem; color: var(--text-tertiary); margin-top: 0.2rem;">Resize & Normalize</div>
                </div>
                <div style="font-size: 1.5rem; color: var(--primary-500);">➔</div>
                <div style="flex: 1.5; min-width: 180px; padding: 1rem; background: rgba(124, 58, 237, 0.08); border: 1px solid var(--border-primary); border-radius: var(--radius-md);">
                    <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">🧠</div>
                    <div style="font-weight: 700; font-size: 0.85rem; color: var(--primary-300);">Parallel CNN Columns</div>
                    <div style="font-size: 0.7rem; color: var(--text-tertiary); margin-top: 0.2rem;">Fine / Med / Coarse Scales</div>
                </div>
                <div style="font-size: 1.5rem; color: var(--primary-500);">➔</div>
                <div style="flex: 1.2; min-width: 160px; padding: 1rem; background: rgba(15,15,26,0.6); border: 1px solid var(--border-secondary); border-radius: var(--radius-md);">
                    <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">🔗</div>
                    <div style="font-weight: 600; font-size: 0.85rem; color: var(--text-primary);">Adaptive Collation</div>
                    <div style="font-size: 0.7rem; color: var(--text-tertiary); margin-top: 0.2rem;">Weight-based Fusion</div>
                </div>
                <div style="font-size: 1.5rem; color: var(--primary-500);">➔</div>
                <div style="flex: 1.2; min-width: 160px; padding: 1rem; background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: var(--radius-md);">
                    <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">🗺️</div>
                    <div style="font-weight: 700; font-size: 0.85rem; color: #34D399;">Density Map Output</div>
                    <div style="font-size: 0.7rem; color: var(--text-tertiary); margin-top: 0.2rem;">Summation Counting</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_section_separator()

    # ── Section 5: Advantages & Applications ──
    col_adv, col_app = st.columns(2)

    with col_adv:
        st.markdown("<h3 style='margin-bottom: 1rem;'>💡 Key Advantages</h3>", unsafe_allow_html=True)
        for adv in ADVANTAGES:
            st.markdown(
                f"""
                <div class="glass-card-flat" style="margin-bottom: 0.8rem; padding: 1rem;">
                    <div style="display: flex; gap: 0.8rem; align-items: start;">
                        <span style="font-size: 1.2rem;">{adv['icon']}</span>
                        <div>
                            <div style="font-weight: 600; font-size: 0.9rem; color: var(--text-primary);">{adv['title']}</div>
                            <div style="font-size: 0.8rem; color: var(--text-tertiary); margin-top: 0.2rem;">{adv['desc']}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_app:
        st.markdown("<h3 style='margin-bottom: 1rem;'>🏟️ Industry Applications</h3>", unsafe_allow_html=True)
        for app in APPLICATIONS:
            st.markdown(
                f"""
                <div class="glass-card-flat" style="margin-bottom: 0.8rem; padding: 1rem;">
                    <div style="display: flex; gap: 0.8rem; align-items: start;">
                        <span style="font-size: 1.2rem;">{app['icon']}</span>
                        <div>
                            <div style="font-weight: 600; font-size: 0.9rem; color: var(--text-primary);">{app['title']}</div>
                            <div style="font-size: 0.8rem; color: var(--text-tertiary); margin-top: 0.2rem;">{app['desc']}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    render_section_separator()

    # ── Section 6: Future Improvements ──
    st.markdown(
        """
        <div class="section-header">
            <span class="section-badge">Evolution</span>
            <h2 class="section-title">Future Scope & Improvements</h2>
            <p class="section-subtitle">Roadmap enhancements planned for the CrowdVision estimation model.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    future_col1, future_col2, future_col3 = st.columns(3)
    for i, fut in enumerate(FUTURE_IMPROVEMENTS):
        current_col = [future_col1, future_col2, future_col3][i % 3]
        with current_col:
            st.markdown(
                f"""
                <div class="glass-card-sm" style="margin-bottom: 1rem; height: calc(100% - 1rem);">
                    <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">{fut['icon']}</div>
                    <h4 style="color: var(--text-primary); margin-bottom: 0.4rem;">{fut['title']}</h4>
                    <p style="font-size: 0.82rem; color: var(--text-tertiary); line-height: 1.5;">{fut['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
