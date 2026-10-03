"""
============================================================
Prediction Page Component — pages/prediction.py
============================================================
Renders the crowd estimation execution page.

Features:
    - Image upload
    - Enhanced MCNN inference
    - Density map
    - Heatmap
    - Model metrics
    - Model-based crowd density level
    - Custom dashboard-style safety alert
============================================================
"""
    
import streamlit as st
from textwrap import dedent
from PIL import Image
import streamlit.components.v1 as components
from ml.inference import predict
from utils.dummy_data import PROCESSING_STEPS

from components.navbar import render_page_header

from components.metrics import render_prediction_metrics

from components.charts import (
    render_density_map_plotly,
    render_heatmap_overlay_plotly,
)

from components.cards import render_gradient_divider

from risk_assessment import assess_crowd_risk


def _render_html(markup, **_kwargs):
    st.html(dedent(markup))


# ============================================================
# CUSTOM ALERT MODAL
# ============================================================

def render_crowd_alert(risk, density_level, crowd_count):
    """
    Display a custom dashboard-style alert modal.

    The modal is intentionally designed to match the existing
    dark/glass dashboard aesthetic instead of using the
    default browser alert().
    """

    # --------------------------------------------------------
    # Critical alert styling
    # --------------------------------------------------------

    if risk["level"] == "CRITICAL":

        border_color = "rgba(239, 68, 68, 0.65)"
        background_color = "rgba(239, 68, 68, 0.08)"
        icon_background = "rgba(239, 68, 68, 0.15)"
        accent = "#F87171"

    # --------------------------------------------------------
    # High density alert styling
    # --------------------------------------------------------

    elif risk["level"] == "DANGER":

        border_color = "rgba(239, 68, 68, 0.55)"
        background_color = "rgba(239, 68, 68, 0.07)"
        icon_background = "rgba(239, 68, 68, 0.13)"
        accent = "#FB7185"

    # --------------------------------------------------------
    # Medium density warning
    # --------------------------------------------------------

    elif risk["level"] == "WARNING":

        border_color = "rgba(245, 158, 11, 0.55)"
        background_color = "rgba(245, 158, 11, 0.07)"
        icon_background = "rgba(245, 158, 11, 0.13)"
        accent = "#FBBF24"

    # --------------------------------------------------------
    # Safe
    # --------------------------------------------------------

    else:

        border_color = "rgba(16, 185, 129, 0.45)"
        background_color = "rgba(16, 185, 129, 0.06)"
        icon_background = "rgba(16, 185, 129, 0.12)"
        accent = "#34D399"

    # --------------------------------------------------------
    # Display normal dashboard status
    # --------------------------------------------------------

    if risk["level"] == "SAFE":

        _render_html(
            f"""
            <div style="
                margin: 0.5rem 0 1.5rem 0;
                padding: 1rem 1.25rem;
                border-radius: 14px;
                border: 1px solid {border_color};
                background: {background_color};
                backdrop-filter: blur(12px);
            ">

                <div style="
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                ">

                    <div style="
                        width: 38px;
                        height: 38px;
                        border-radius: 10px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        background: {icon_background};
                        color: {accent};
                        font-size: 1.25rem;
                        font-weight: 700;
                    ">
                        ✓
                    </div>

                    <div>

                        <div style="
                            color: {accent};
                            font-size: 0.95rem;
                            font-weight: 700;
                        ">
                            Crowd Density Normal
                        </div>

                        <div style="
                            color: var(--text-tertiary);
                            font-size: 0.78rem;
                            margin-top: 3px;
                        ">
                            Density Level: {density_level}
                        </div>

                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    # --------------------------------------------------------
    # WARNING / DANGER / CRITICAL dashboard status
    # --------------------------------------------------------

    _render_html(
        f"""
        <div style="
            margin: 0.5rem 0 1.5rem 0;
            padding: 1rem 1.25rem;
            border-radius: 14px;
            border: 1px solid {border_color};
            background: {background_color};
            backdrop-filter: blur(12px);
        ">

            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
            ">

                <div style="
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                ">

                    <div style="
                        width: 42px;
                        height: 42px;
                        border-radius: 11px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        background: {icon_background};
                        color: {accent};
                        font-size: 1.25rem;
                    ">
                        {risk["emoji"]}
                    </div>

                    <div>

                        <div style="
                            color: {accent};
                            font-size: 0.95rem;
                            font-weight: 700;
                        ">
                            {risk["title"]}
                        </div>

                        <div style="
                            color: var(--text-tertiary);
                            font-size: 0.78rem;
                            margin-top: 3px;
                        ">
                            Density Level: {density_level}
                        </div>

                    </div>

                </div>

                <div style="
                    text-align: right;
                    min-width: 100px;
                ">

                    <div style="
                        color: var(--text-tertiary);
                        font-size: 0.7rem;
                    ">
                        ESTIMATED CROWD
                    </div>

                    <div style="
                        color: var(--text-primary);
                        font-size: 1.25rem;
                        font-weight: 700;
                    ">
                        {crowd_count}
                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CUSTOM POPUP
# ============================================================

def render_browser_style_alert(risk, density_level, crowd_count):
    """
    Render a browser-style custom alert using the same visual
    language as the dashboard.

    A native JavaScript alert cannot be styled with webpage CSS,
    therefore this creates a custom modal-style popup.
    """

    if risk["level"] == "CRITICAL":

        accent = "#F87171"
        glow = "rgba(239, 68, 68, 0.30)"
        icon = "🚨"

    else:

        accent = "#FB7185"
        glow = "rgba(239, 68, 68, 0.25)"
        icon = "⚠️"

    st.components.v1.html(
        f"""
        <!DOCTYPE html>
        <html>

        <head>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                padding: 0;
                font-family:
                    Inter,
                    -apple-system,
                    BlinkMacSystemFont,
                    "Segoe UI",
                    sans-serif;

                background: transparent;
            }}

            .alert-wrapper {{
                position: fixed;
                inset: 0;

                display: flex;
                align-items: center;
                justify-content: center;

                z-index: 999999;

                background: rgba(2, 6, 23, 0.72);

                backdrop-filter: blur(7px);
            }}

            .alert-box {{
                width: min(430px, 90vw);

                padding: 28px;

                border-radius: 20px;

                background:
                    linear-gradient(
                        145deg,
                        rgba(15, 23, 42, 0.98),
                        rgba(17, 24, 39, 0.98)
                    );

                border: 1px solid {accent};

                box-shadow:
                    0 0 0 1px rgba(255,255,255,0.03),
                    0 25px 70px rgba(0,0,0,0.55),
                    0 0 45px {glow};

                color: #F8FAFC;

                animation: popup 0.25s ease-out;
            }}

            @keyframes popup {{

                from {{
                    opacity: 0;
                    transform: scale(0.92) translateY(10px);
                }}

                to {{
                    opacity: 1;
                    transform: scale(1) translateY(0);
                }}

            }}

            .alert-icon {{
                width: 58px;
                height: 58px;

                border-radius: 16px;

                display: flex;
                align-items: center;
                justify-content: center;

                margin-bottom: 18px;

                background: rgba(239, 68, 68, 0.12);

                font-size: 27px;

                box-shadow:
                    0 0 25px {glow};
            }}

            .alert-label {{
                color: {accent};

                font-size: 11px;

                font-weight: 700;

                letter-spacing: 1.4px;

                text-transform: uppercase;

                margin-bottom: 7px;
            }}

            .alert-title {{
                font-size: 22px;

                font-weight: 700;

                margin-bottom: 10px;
            }}

            .alert-message {{
                color: #94A3B8;

                font-size: 13px;

                line-height: 1.6;

                margin-bottom: 20px;
            }}

            .alert-info {{
                display: flex;

                justify-content: space-between;

                align-items: center;

                padding: 13px 15px;

                border-radius: 12px;

                background: rgba(255,255,255,0.04);

                border:
                    1px solid rgba(255,255,255,0.07);

                margin-bottom: 20px;
            }}

            .info-label {{
                color: #64748B;

                font-size: 10px;

                letter-spacing: 0.8px;

                text-transform: uppercase;
            }}

            .info-value {{
                color: #F8FAFC;

                font-size: 15px;

                font-weight: 700;
            }}

            .close-button {{
                width: 100%;

                border: none;

                border-radius: 10px;

                padding: 11px;

                background: {accent};

                color: #0F172A;

                font-size: 13px;

                font-weight: 700;

                cursor: pointer;
            }}

            .close-button:hover {{
                opacity: 0.9;
            }}

        </style>

        </head>

        <body>

            <div class="alert-wrapper">

                <div class="alert-box">

                    <div class="alert-icon">
                        {icon}
                    </div>

                    <div class="alert-label">
                        CrowdVision AI • Safety Alert
                    </div>

                    <div class="alert-title">
                        {risk["title"]}
                    </div>

                    <div class="alert-message">
                        {risk["message"]}
                    </div>

                    <div class="alert-info">

                        <div>
                            <div class="info-label">
                                Density Level
                            </div>

                            <div class="info-value">
                                {density_level}
                            </div>
                        </div>

                        <div style="text-align:right;">

                            <div class="info-label">
                                Estimated Crowd
                            </div>

                            <div class="info-value">
                                {crowd_count}
                            </div>

                        </div>

                    </div>

                    <button
                        class="close-button"
                        onclick="closeAlert()"
                    >
                        Acknowledge Alert
                    </button>

                </div>

            </div>

            <script>

                function closeAlert() {{
                    document.querySelector(
                        ".alert-wrapper"
                    ).style.display = "none";
                }}

            </script>

        </body>

        </html>
        """,
        height=430,
    )


# ============================================================
# MAIN PREDICTION PAGE
# ============================================================

def render_prediction_page():
    """Render the Prediction Page content."""

    render_page_header(
        title="Crowd Estimation Engine",
        subtitle=(
            "Upload a crowd image to run the Enhanced MCNN "
            "pipeline and estimate density mapping."
        ),
        badge_text="Real-Time Inference",
    )

    # ========================================================
    # UPLOAD SECTION
    # ========================================================

    _render_html(
        """
        <div class="glass-card animate-fade-in-up"
             style="margin-bottom: 2rem;">

            <h3 class="gradient-text"
                style="margin-bottom: 0.5rem;">

                Upload Crowd Image

            </h3>

            <p style="
                font-size: 0.85rem;
                color: var(--text-tertiary);
            ">

                Supports JPEG, PNG, or BMP formats.
                The model will run multi-scale receptive
                field analysis on the uploaded image.

            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # FILE UPLOADER
    # ========================================================

    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png", "bmp"],
        label_visibility="collapsed",
    )

    # ========================================================
    # IMAGE UPLOADED
    # ========================================================

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        # ----------------------------------------------------
        # Unique file identifier
        # ----------------------------------------------------

        file_hash = (
            f"{uploaded_file.name}_{uploaded_file.size}"
        )

        # ----------------------------------------------------
        # Initialize prediction state
        # ----------------------------------------------------

        if (
            "last_uploaded_file" not in st.session_state
            or st.session_state.last_uploaded_file != file_hash
        ):

            st.session_state.last_uploaded_file = file_hash

            st.session_state.prediction_done = False

            st.session_state.prediction_results = None

            # Reset popup state for new image
            st.session_state.alert_shown_for_file = False

        # ====================================================
        # PREVIEW + CONTROLS
        # ====================================================

        col_preview, col_proc = st.columns([1, 1])

        # ----------------------------------------------------
        # IMAGE PREVIEW
        # ----------------------------------------------------

        with col_preview:

            _render_html(
                "<h4>Uploaded Image Preview</h4>",
                unsafe_allow_html=True,
            )

            st.image(
                image,
                use_container_width=True,
                caption=(
                    f"File: {uploaded_file.name} | "
                    f"Resolution: {image.width} × {image.height}"
                ),
            )

        # ----------------------------------------------------
        # ANALYSIS CONTROLS
        # ----------------------------------------------------

        with col_proc:

            _render_html(
                "<h4>Analysis Controls</h4>",
                unsafe_allow_html=True,
            )

            # =================================================
            # START ANALYSIS
            # =================================================

            if not st.session_state.prediction_done:

                st.write("")

                if st.button(
                    "🚀 Analyze Crowd Image",
                    type="primary",
                    use_container_width=True,
                ):

                    status_area = st.empty()

                    progress_bar = st.progress(0)

                    total_steps = len(PROCESSING_STEPS)

                    # -----------------------------------------
                    # Processing animation
                    # -----------------------------------------

                    for i, step in enumerate(
                        PROCESSING_STEPS
                    ):

                        status_area.markdown(
                            f"""
                            <div class="processing-step active
                                        animate-shimmer">

                                <span class="step-icon">
                                    {step['icon']}
                                </span>

                                <span class="step-text active">
                                    Step {i + 1}/{total_steps}:
                                    {step['text']}
                                </span>

                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        progress_bar.progress(
                            int(
                                (i + 1)
                                / total_steps
                                * 100
                            )
                        )

                    status_area.empty()

                    progress_bar.empty()

                    # -----------------------------------------
                    # Actual model inference
                    # -----------------------------------------

                    st.session_state.prediction_results = (
                        predict(image)
                    )

                    st.session_state.prediction_done = True

                    st.session_state.alert_shown_for_file = False

                    st.success(
                        "✅ Crowd density estimation "
                        "completed successfully!"
                    )

                    st.rerun()

                else:

                    st.info(
                        "Click 'Analyze Crowd Image' to trigger "
                        "the Enhanced MCNN prediction pipeline."
                    )

            # =================================================
            # ANALYSIS COMPLETED
            # =================================================

            else:

                _render_html(
                    """
                    <div class="glass-card-sm"
                         style="
                            border-color:
                                rgba(16, 185, 129, 0.3);

                            background:
                                rgba(16, 185, 129, 0.04);
                         ">

                        <div style="
                            display: flex;
                            align-items: center;
                            gap: 0.5rem;
                            color: #34D399;
                            font-weight: 600;
                        ">

                            <span>✅</span>

                            Pipeline Execution Completed

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # ---------------------------------------------
                # RESET
                # ---------------------------------------------

                if st.button(
                    "🔄 Reset / Analyze Again",
                    use_container_width=True,
                ):

                    st.session_state.prediction_done = False

                    st.session_state.prediction_results = None

                    st.session_state.alert_shown_for_file = False

                    st.rerun()

        # ========================================================
        # RESULTS
        # ========================================================

        if (
            st.session_state.prediction_done
            and st.session_state.prediction_results
            is not None
        ):

            results = (
                st.session_state.prediction_results
            )

            # ====================================================
            # MODEL DENSITY LEVEL
            # ====================================================

            # IMPORTANT:
            # We are using YOUR model's existing density_level.
            #
            # inference.py already calculates:
            #
            # Low
            # Medium
            # High
            # Very High

            density_level = results["density_level"]

            # ====================================================
            # MODEL CROWD COUNT
            # ====================================================

            # Use the count already calculated by inference.py.

            predicted_count = results["crowd_count"]

            # ====================================================
            # RISK ASSESSMENT
            # ====================================================

            risk = assess_crowd_risk(
                density_level
            )

            # ====================================================
            # SHOW DASHBOARD STATUS
            # ====================================================

            render_crowd_alert(
                risk=risk,
                density_level=density_level,
                crowd_count=predicted_count,
            )

            # ====================================================
            # SHOW POPUP ONLY FOR HIGH / VERY HIGH
            # ====================================================

            if risk["level"] in [
                "DANGER",
                "CRITICAL",
            ]:

                if not st.session_state.alert_shown_for_file:

                    st.session_state.alert_shown_for_file = True

                    render_browser_style_alert(
                        risk=risk,
                        density_level=density_level,
                        crowd_count=predicted_count,
                    )

            # ====================================================
            # RESULTS HEADER
            # ====================================================

            render_gradient_divider()

            _render_html(
                """
                <div class="section-header"
                     style="margin-bottom: 1.5rem;">

                    <span class="section-badge"
                          style="
                            background:
                                rgba(16, 185, 129, 0.1);

                            color: #34D399;

                            border-color:
                                rgba(16, 185, 129, 0.25);
                          ">

                        Estimation Results

                    </span>

                    <h2 class="section-title">
                        Pipeline Output
                    </h2>

                </div>
                """,
                unsafe_allow_html=True,
            )

            # ====================================================
            # KPI METRICS
            # ====================================================

            render_prediction_metrics(results)

            _render_html(
                "<div style='height: 1.5rem;'></div>",
                unsafe_allow_html=True,
            )

            # ====================================================
            # VISUAL MAPS
            # ====================================================

            col_orig, col_dens, col_heat = st.columns(3)

            # ----------------------------------------------------
            # ORIGINAL IMAGE
            # ----------------------------------------------------

            with col_orig:

                _render_html(
                    """
                    <div class="image-frame">

                        <div class="image-caption">
                            Input Image
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.image(
                    image,
                    use_container_width=True,
                )

            # ----------------------------------------------------
            # DENSITY MAP
            # ----------------------------------------------------

            with col_dens:

                _render_html(
                    """
                    <div class="image-frame">

                        <div class="image-caption">
                            Enhanced MCNN Density Map
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                density_map = results["density_map"]

                render_density_map_plotly(
                    density_map,
                    title="",
                )

            # ----------------------------------------------------
            # HEATMAP
            # ----------------------------------------------------

            with col_heat:

                _render_html(
                    """
                    <div class="image-frame">

                        <div class="image-caption">
                            Intensity Heatmap Overlay
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                heatmap = results["density_map"]

                render_heatmap_overlay_plotly(
                    heatmap,
                    title="",
                )

            _render_html(
                "<div style='height: 1.5rem;'></div>",
                unsafe_allow_html=True,
            )

            # ====================================================
            # DETAILS + ACTIONS
            # ====================================================

            col_info, col_actions = st.columns([2, 1])

            # ----------------------------------------------------
            # EXECUTION PARAMETERS
            # ----------------------------------------------------

            with col_info:

                _render_html(
                    f"""
                    <div class="glass-card-sm"
                         style="height: 100%;">

                        <h4>
                            ⚙️ Execution Parameters
                        </h4>

                        <table style="
                            width: 100%;
                            border-collapse: collapse;
                            margin-top: 0.5rem;
                            font-size: 0.85rem;
                            color: var(--text-secondary);
                        ">

                            <tr style="
                                border-bottom:
                                1px solid
                                rgba(255,255,255,0.06);
                            ">

                                <td style="
                                    padding: 0.5rem 0;
                                    font-weight: 500;
                                ">
                                    Core Architecture
                                </td>

                                <td style="
                                    text-align: right;
                                "
                                class="font-mono">

                                    {results['model_version']}

                                </td>

                            </tr>

                            <tr style="
                                border-bottom:
                                1px solid
                                rgba(255,255,255,0.06);
                            ">

                                <td style="
                                    padding: 0.5rem 0;
                                    font-weight: 500;
                                ">
                                    Input Resolution
                                </td>

                                <td style="
                                    text-align: right;
                                "
                                class="font-mono">

                                    {results['input_resolution']} px

                                </td>

                            </tr>

                            <tr style="
                                border-bottom:
                                1px solid
                                rgba(255,255,255,0.06);
                            ">

                                <td style="
                                    padding: 0.5rem 0;
                                    font-weight: 500;
                                ">
                                    Collation Resolution
                                </td>

                                <td style="
                                    text-align: right;
                                "
                                class="font-mono">

                                    {results['density_map_resolution']} px

                                </td>

                            </tr>

                            <tr>

                                <td style="
                                    padding: 0.5rem 0;
                                    font-weight: 500;
                                ">
                                    Collation Method
                                </td>

                                <td style="
                                    text-align: right;
                                    color: var(--primary-300);
                                ">

                                    Adaptive Receptive
                                    Fields Fusion

                                </td>

                            </tr>

                        </table>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # ----------------------------------------------------
            # EXPORT OPTIONS
            # ----------------------------------------------------

            with col_actions:

                _render_html(
                    """
                    <div class="glass-card-sm text-center"
                         style="
                            height: 100%;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            gap: 1rem;
                         ">

                        <h4 style="margin: 0;">
                            Export Options
                        </h4>

                        <p style="
                            font-size: 0.78rem;
                            color: var(--text-tertiary);
                            margin: 0;
                        ">

                            Download a full PDF summary containing
                            input image, predicted maps, count
                            details, and confidence logs.

                        </p>
                    """,
                    unsafe_allow_html=True,
                )

                st.button(
                    "📥 Download Analysis Report",
                    use_container_width=True,
                    key="dl_report",
                )

                _render_html(
                    "</div>",
                    unsafe_allow_html=True,
                )

    # ============================================================
    # NO IMAGE UPLOADED
    # ============================================================

    else:

        _render_html(
            """
            <div class="glass-card text-center
                        animate-fade-in-up"
                 style="
                    padding: 4rem 2rem;
                    border-style: dashed;
                    border-color: var(--border-primary);
                 ">

                <div style="
                    font-size: 4rem;
                    margin-bottom: 1rem;
                ">
                    🖼️
                </div>

                <h3>
                    No Image Uploaded
                </h3>

                <p style="
                    max-width: 500px;
                    margin:
                        0.5rem auto 1.5rem auto;
                    color: var(--text-tertiary);
                ">

                    Please drag and drop a crowd scene image
                    or browse your local directory using the
                    uploader above to run the estimation model.

                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )