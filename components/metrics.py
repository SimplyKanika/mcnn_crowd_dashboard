"""
============================================================
Metrics Component — KPI & Metric Display Widgets
============================================================
Provides functions to render KPI rows, metric displays,
and animated counter-style stat sections.
============================================================
"""

import streamlit as st
from components.cards import render_metric_card


# ── Color rotation for metric cards ──
METRIC_COLORS = ["purple", "blue", "emerald", "amber", "rose", "cyan"]


def render_kpi_row(kpis):
    """
    Render a row of KPI metric cards.

    Args:
        kpis: List of dicts with 'icon', 'value', 'label', and
              optional 'color' keys.
    """
    cols = st.columns(len(kpis))
    for i, (col, kpi) in enumerate(zip(cols, kpis)):
        with col:
            render_metric_card(
                icon=kpi["icon"],
                value=kpi["value"],
                label=kpi["label"],
                color=kpi.get("color", METRIC_COLORS[i % len(METRIC_COLORS)]),
            )


def render_hero_stats(stats):
    """
    Render hero section animated statistic cards.

    Args:
        stats: List of dicts with 'icon', 'value', 'label', 'color' keys.
    """
    cols = st.columns(len(stats))
    for col, stat in zip(cols, stats):
        with col:
            render_metric_card(
                icon=stat["icon"],
                value=stat["value"],
                label=stat["label"],
                color=stat.get("color", "purple"),
            )


def render_kpi_dashboard(kpi_data):
    """
    Render a complete KPI dashboard section with two rows.

    Args:
        kpi_data: Dict from get_kpi_summary() in dummy_data.
    """
    # First row — Primary KPIs
    row1 = [
        {"icon": "📊", "value": f"{kpi_data['total_predictions']:,}",
         "label": "Total Predictions", "color": "purple"},
        {"icon": "👥", "value": str(kpi_data["avg_crowd_count"]),
         "label": "Avg Crowd Count", "color": "blue"},
        {"icon": "📉", "value": str(kpi_data["min_count"]),
         "label": "Min Count", "color": "emerald"},
        {"icon": "📈", "value": str(kpi_data["max_count"]),
         "label": "Max Count", "color": "rose"},
    ]
    render_kpi_row(row1)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Second row — Secondary KPIs
    row2 = [
        {"icon": "🎯", "value": f"{kpi_data['avg_confidence']}%",
         "label": "Avg Confidence", "color": "amber"},
        {"icon": "⚡", "value": f"{kpi_data['avg_inference_time']}s",
         "label": "Avg Inference Time", "color": "cyan"},
        {"icon": "🖼️", "value": f"{kpi_data['total_images']:,}",
         "label": "Total Images", "color": "purple"},
        {"icon": "🟢", "value": kpi_data["uptime"],
         "label": "System Uptime", "color": "emerald"},
    ]
    render_kpi_row(row2)


def render_prediction_metrics(results):
    """
    Render prediction result metrics in a styled row.

    Args:
        results: Dict from get_prediction_results() in dummy_data.
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card(
            icon="👥",
            value=str(results["crowd_count"]),
            label="Crowd Count",
            color="purple",
        )

    with col2:
        render_metric_card(
            icon="🎯",
            value=f"{results['confidence']}%",
            label="Confidence",
            color="emerald",
        )

    with col3:
        render_metric_card(
            icon="⚡",
            value=f"{results['inference_time']}s",
            label="Inference Time",
            color="blue",
        )

    with col4:
        render_metric_card(
            icon="📊",
            value=results["density_level"],
            label="Density Level",
            color="amber",
        )
