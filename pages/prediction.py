"""
============================================================
Prediction Page Component — pages/prediction.py
============================================================
Renders the crowd estimation execution page.
Allows uploading an image, triggers a simulated multi-step AI
processing pipeline, and displays the original image next to
the generated crowd density and intensity maps along with
estimated metrics.
============================================================
"""

import streamlit as st
import time
from PIL import Image
import numpy as np
from utils.dummy_data import (
    PROCESSING_STEPS,
    get_prediction_results,
    generate_dummy_density_map,
    generate_dummy_heatmap,
)
from components.navbar import render_page_header
from components.cards import (
    render_density_badge,
    render_badge,
    render_gradient_divider,
)
from components.metrics import render_prediction_metrics
from components.charts import (
    render_density_map_plotly,
    render_heatmap_overlay_plotly,
)


def render_prediction_page():
    """Render the Prediction Page content."""
    render_page_header(
        title="Crowd Estimation Engine",
        subtitle="Upload a crowd image to run the Enhanced MCNN pipeline and estimate density mapping.",
        badge_text="Real-Time Inference",
    )

    # ── Upload Section ──
    st.markdown(
        """
        <div class="glass-card animate-fade-in-up" style="margin-bottom: 2rem;">
            <h3 class="gradient-text" style="margin-bottom: 0.5rem;">Upload Crowd Image</h3>
            <p style="font-size: 0.85rem; color: var(--text-tertiary);">
                Supports JPEG, PNG, or BMP formats. The model will run multi-scale receptive field analysis on the uploaded image.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Use native Streamlit file uploader styled via custom CSS
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png", "bmp"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        # Load the image
        image = Image.open(uploaded_file)
        
        # Calculate a unique key for the uploaded file to detect new uploads
        file_hash = f"{uploaded_file.name}_{uploaded_file.size}"

        # Initialize session state for prediction results
        if "last_uploaded_file" not in st.session_state or st.session_state.last_uploaded_file != file_hash:
            st.session_state.last_uploaded_file = file_hash
            st.session_state.prediction_done = False
            st.session_state.prediction_results = None

        col_preview, col_proc = st.columns([1, 1])

        with col_preview:
            st.markdown("<h4>Uploaded Image Preview</h4>", unsafe_allow_html=True)
            # Display image in a styled frame
            st.image(image, use_container_width=True, caption=f"File: {uploaded_file.name} | Resolution: {image.width} × {image.height}")

        with col_proc:
            st.markdown("<h4>Analysis Controls</h4>", unsafe_allow_html=True)
            
            # Start prediction button
            if not st.session_state.prediction_done:
                st.write("")
                if st.button("🚀 Analyze Crowd Image", type="primary", use_container_width=True):
                    # Trigger simulated processing
                    status_area = st.empty()
                    progress_bar = st.progress(0)
                    
                    total_steps = len(PROCESSING_STEPS)
                    
                    for i, step in enumerate(PROCESSING_STEPS):
                        # Update status text using styled HTML
                        status_area.markdown(
                            f"""
                            <div class="processing-step active animate-shimmer">
                                <span class="step-icon">{step['icon']}</span>
                                <span class="step-text active">Step {i+1}/{total_steps}: {step['text']}</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        
                        # Simulate step work
                        time.sleep(step["duration"])
                        
                        # Update progress
                        progress_bar.progress(int((i + 1) / total_steps * 100))
                    
                    # Clear progress bars and status
                    status_area.empty()
                    progress_bar.empty()
                    
                    # Set results
                    st.session_state.prediction_results = get_prediction_results()
                    st.session_state.prediction_done = True
                    st.success("✅ Crowd density estimation completed successfully!")
                    st.rerun()
                else:
                    st.info("Click 'Analyze Crowd Image' to trigger the Enhanced MCNN prediction pipeline.")
            else:
                st.markdown(
                    """
                    <div class="glass-card-sm" style="border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.04);">
                        <div style="display: flex; align-items: center; gap: 0.5rem; color: #34D399; font-weight: 600;">
                            <span>✅</span> Pipeline Execution Completed
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("🔄 Reset / Analyze Again", use_container_width=True):
                    st.session_state.prediction_done = False
                    st.session_state.prediction_results = None
                    st.rerun()

        # ── Results Area ──
        if st.session_state.prediction_done and st.session_state.prediction_results is not None:
            results = st.session_state.prediction_results
            
            render_gradient_divider()
            
            st.markdown(
                """
                <div class="section-header" style="margin-bottom: 1.5rem;">
                    <span class="section-badge" style="background: rgba(16, 185, 129, 0.1); color: #34D399; border-color: rgba(16, 185, 129, 0.25);">Estimation Results</span>
                    <h2 class="section-title">Pipeline Output</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Render KPI Metric Cards for crowd estimation
            render_prediction_metrics(results)
            
            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

            # Columns for visual maps
            col_orig, col_dens, col_heat = st.columns(3)

            with col_orig:
                st.markdown(
                    """
                    <div class="image-frame">
                        <div class="image-caption">Input Image</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.image(image, use_container_width=True)

            with col_dens:
                st.markdown(
                    """
                    <div class="image-frame">
                        <div class="image-caption">Enhanced MCNN Density Map</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                # Generate and render density map
                density_map = generate_dummy_density_map()
                render_density_map_plotly(density_map, title="")

            with col_heat:
                st.markdown(
                    """
                    <div class="image-frame">
                        <div class="image-caption">Intensity Heatmap Overlay</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                # Generate and render heatmap
                heatmap = generate_dummy_heatmap()
                render_heatmap_overlay_plotly(heatmap, title="")

            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

            # Details and Action Buttons
            col_info, col_actions = st.columns([2, 1])
            
            with col_info:
                st.markdown(
                    f"""
                    <div class="glass-card-sm" style="height: 100%;">
                        <h4>⚙️ Execution Parameters</h4>
                        <table style="width: 100%; border-collapse: collapse; margin-top: 0.5rem; font-size: 0.85rem; color: var(--text-secondary);">
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                                <td style="padding: 0.5rem 0; font-weight: 500;">Core Architecture</td>
                                <td style="text-align: right;" class="font-mono">{results['model_version']}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                                <td style="padding: 0.5rem 0; font-weight: 500;">Input Resolution</td>
                                <td style="text-align: right;" class="font-mono">{results['input_resolution']} px</td>
                            </tr>
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                                <td style="padding: 0.5rem 0; font-weight: 500;">Collation Resolution</td>
                                <td style="text-align: right;" class="font-mono">{results['density_map_resolution']} px</td>
                            </tr>
                            <tr>
                                <td style="padding: 0.5rem 0; font-weight: 500;">Collation Method</td>
                                <td style="text-align: right; color: var(--primary-300);">Adaptive Receptive Fields Fusion</td>
                            </tr>
                        </table>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_actions:
                st.markdown(
                    """
                    <div class="glass-card-sm text-center" style="height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 1rem;">
                        <h4 style="margin: 0;">Export Options</h4>
                        <p style="font-size: 0.78rem; color: var(--text-tertiary); margin: 0;">
                            Download a full PDF summary containing input image, predicted maps, count details, and confidence logs.
                        </p>
                    """,
                    unsafe_allow_html=True,
                )
                
                # Non-functional download button
                st.button("📥 Download Analysis Report", use_container_width=True, key="dl_report")
                st.markdown("</div>", unsafe_allow_html=True)
                
    else:
        # Placeholder view when no image is uploaded
        st.markdown(
            """
            <div class="glass-card text-center animate-fade-in-up" style="padding: 4rem 2rem; border-style: dashed; border-color: var(--border-primary);">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🖼️</div>
                <h3>No Image Uploaded</h3>
                <p style="max-width: 500px; margin: 0.5rem auto 1.5rem auto; color: var(--text-tertiary);">
                    Please drag and drop a crowd scene image or browse your local directory using the uploader above to run the estimation model.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
