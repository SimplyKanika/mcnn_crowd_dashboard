"""
============================================================
Analytics Page Component — pages/analytics.py
============================================================
Renders the analytics and KPI insights page.
Provides tabs for executive summary, trend lines, and
distribution maps using interactive Plotly charts and
the system's dummy data generator.
============================================================
"""

import streamlit as st
from utils.dummy_data import (
    get_kpi_summary,
    get_daily_predictions,
    get_weekly_predictions,
    get_monthly_predictions,
    get_density_distribution,
    get_crowd_count_histogram,
    get_hourly_heatmap_data,
    get_scatter_data,
)
from components.navbar import render_page_header
from components.metrics import render_kpi_dashboard
from components.charts import (
    render_line_chart,
    render_multi_line_chart,
    render_bar_chart,
    render_pie_chart,
    render_histogram,
    render_area_chart,
    render_heatmap,
    render_scatter_plot,
)


def render_analytics_page():
    """Render the Analytics Page content."""
    render_page_header(
        title="Predictive Analytics Dashboard",
        subtitle="Historical logs and statistical analysis of MCNN prediction counts, confidence, and system KPIs.",
        badge_text="System Insights",
    )

    # Fetch fresh dummy/simulated data
    kpis = get_kpi_summary()
    daily_df = get_daily_predictions()
    weekly_df = get_weekly_predictions()
    monthly_df = get_monthly_predictions()
    density_df = get_density_distribution()
    hist_df = get_crowd_count_histogram()
    heatmap_df = get_hourly_heatmap_data()
    scatter_df = get_scatter_data()

    # ── Master KPI Section ──
    st.markdown("<h3>System Key Performance Indicators</h3>", unsafe_allow_html=True)
    render_kpi_dashboard(kpis)

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # ── Tabs layout for Analytics Charts ──
    tab1, tab2, tab3 = st.columns([1, 1, 1])
    
    # We will use native Streamlit tabs for high-quality dashboard separation
    tab_exec, tab_trends, tab_dist = st.tabs([
        "📊 Executive Summary",
        "📈 Predictive Trends",
        "🌡️ Distributions & Correlations"
    ])

    with tab_exec:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        col_exec_l, col_exec_r = st.columns(2)
        
        with col_exec_l:
            st.markdown(
                """
                <div class="chart-container">
                    <div class="chart-title">📈 Overall Prediction Trend (Past 30 Days)</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            render_line_chart(
                df=daily_df,
                x="Date",
                y="Crowd Count",
                title="",
                height=350
            )

        with col_exec_r:
            st.markdown(
                """
                <div class="chart-container">
                    <div class="chart-title">🍕 Predicted Density Level Distribution</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            render_pie_chart(
                df=density_df,
                names="Density Level",
                values="Count",
                title="",
                colors=density_df["Color"].tolist(),
                height=350
            )

    with tab_trends:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        col_trend_l, col_trend_r = st.columns(2)

        with col_trend_l:
            st.markdown(
                """
                <div class="chart-container">
                    <div class="chart-title">📊 Average Weekly Counts</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            render_bar_chart(
                df=weekly_df,
                x="Week",
                y="Avg Crowd Count",
                title="",
                height=350
            )

        with col_trend_r:
            st.markdown(
                """
                <div class="chart-container">
                    <div class="chart-title">📉 Cumulative Area Count Trend</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            render_area_chart(
                df=daily_df,
                x="Date",
                y="Crowd Count",
                title="",
                height=350
            )
            
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        # Monthly performance comparison full-width
        st.markdown(
            """
            <div class="chart-container">
                <div class="chart-title">🗓️ Monthly Metrics Comparison (Volume vs. Counts)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_multi_line_chart(
            df=monthly_df,
            x="Month",
            y_columns=["Avg Crowd Count", "Total Predictions"],
            title="",
            height=350
        )

    with tab_dist:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        # Heatmap full-width
        st.markdown(
            """
            <div class="chart-container">
                <div class="chart-title">🌡️ Hourly Crowd Density Concentration (Day vs. Hour)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_heatmap(
            df=heatmap_df,
            x="Hour",
            y="Day",
            z="Count",
            title="",
            height=400
        )
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        col_dist_l, col_dist_r = st.columns(2)
        
        with col_dist_l:
            st.markdown(
                """
                <div class="chart-container">
                    <div class="chart-title">📊 Frequency Distribution of Counts</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            render_histogram(
                df=hist_df,
                column="Crowd Count",
                title="",
                nbins=25,
                height=350
            )

        with col_dist_r:
            st.markdown(
                """
                <div class="chart-container">
                    <div class="chart-title">🎯 Density Count vs. Model Confidence Correlation</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            render_scatter_plot(
                df=scatter_df,
                x="Crowd Count",
                y="Confidence (%)",
                title="",
                height=350
            )
            
    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # Bottom helper info card
    st.markdown(
        """
        <div class="glass-card-sm animate-fade-in-up" style="background: rgba(124, 58, 237, 0.03);">
            <h4 style="margin-bottom: 0.5rem;">📊 Data Sourcing & Simulation Note</h4>
            <p style="font-size: 0.85rem; color: var(--text-tertiary); margin: 0; line-height: 1.6;">
                The metrics, logs, and graphs illustrated above are derived from simulated databases mimicking predictions
                on ShanghaiTech Part A & B benchmark datasets. These analytics illustrate the historical counts,
                density correlations, and accuracy levels of the collation layer over extended periods of deployment.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
