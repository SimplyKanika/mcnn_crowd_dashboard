"""
============================================================
Charts Component — Reusable Plotly Chart Wrappers
============================================================
Provides functions to create premium-styled Plotly charts
with the dark theme color palette. All charts are interactive
and use consistent styling.
============================================================
"""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np


# ── Shared Layout Configuration ──
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#94A3B8", size=12),
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(
        bgcolor="rgba(26, 26, 46, 0.8)",
        bordercolor="rgba(255,255,255,0.06)",
        borderwidth=1,
        font=dict(size=11),
    ),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        zerolinecolor="rgba(255,255,255,0.06)",
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        zerolinecolor="rgba(255,255,255,0.06)",
    ),
    hoverlabel=dict(
        bgcolor="#1A1A2E",
        bordercolor="#7C3AED",
        font=dict(family="Inter, sans-serif", color="#F1F5F9", size=13),
    ),
)

# ── Color Palette ──
COLORS = {
    "primary": "#7C3AED",
    "blue": "#3B82F6",
    "cyan": "#06B6D4",
    "emerald": "#10B981",
    "amber": "#F59E0B",
    "rose": "#F43F5E",
    "pink": "#EC4899",
    "purple_light": "#A78BFA",
    "blue_light": "#60A5FA",
}

COLOR_SEQUENCE = [
    "#7C3AED", "#3B82F6", "#06B6D4", "#10B981",
    "#F59E0B", "#F43F5E", "#EC4899", "#A78BFA",
]


def _apply_layout(fig, title="", height=400):
    """Apply consistent layout to any Plotly figure."""
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(
            text=title,
            font=dict(family="Outfit, sans-serif", size=16, color="#F1F5F9"),
            x=0.02,
        ),
        height=height,
    )
    return fig


def render_line_chart(df, x, y, title="", color=None, height=400):
    """
    Render an interactive line chart.

    Args:
        df: Pandas DataFrame.
        x: Column name for x-axis.
        y: Column name (or list) for y-axis.
        title: Chart title.
        color: Line color (defaults to primary purple).
        height: Chart height in pixels.
    """
    color = color or COLORS["primary"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y],
        mode="lines+markers",
        line=dict(color=color, width=2.5, shape="spline"),
        marker=dict(size=5, color=color),
        fill="tozeroy",
        fillcolor=f"rgba({_hex_to_rgb(color)}, 0.08)",
        hovertemplate=f"<b>{x}</b>: %{{x}}<br><b>{y}</b>: %{{y}}<extra></extra>",
    ))
    fig = _apply_layout(fig, title, height)
    st.plotly_chart(fig, use_container_width=True)


def render_multi_line_chart(df, x, y_columns, title="", height=400):
    """
    Render a multi-line chart with multiple y columns.

    Args:
        df: Pandas DataFrame.
        x: Column name for x-axis.
        y_columns: List of column names for y-axis lines.
        title: Chart title.
        height: Chart height.
    """
    fig = go.Figure()
    for i, col in enumerate(y_columns):
        color = COLOR_SEQUENCE[i % len(COLOR_SEQUENCE)]
        fig.add_trace(go.Scatter(
            x=df[x], y=df[col],
            mode="lines+markers",
            name=col,
            line=dict(color=color, width=2.5, shape="spline"),
            marker=dict(size=5, color=color),
        ))
    fig = _apply_layout(fig, title, height)
    st.plotly_chart(fig, use_container_width=True)


def render_bar_chart(df, x, y, title="", color=None, height=400):
    """
    Render an interactive bar chart.

    Args:
        df: Pandas DataFrame.
        x: Column name for x-axis.
        y: Column name for y-axis.
        title: Chart title.
        color: Bar color.
        height: Chart height.
    """
    color = color or COLORS["blue"]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df[x], y=df[y],
        marker=dict(
            color=df[y],
            colorscale=[[0, "#3B82F6"], [0.5, "#7C3AED"], [1, "#EC4899"]],
            line=dict(width=0),
            cornerradius=6,
        ),
        hovertemplate=f"<b>{x}</b>: %{{x}}<br><b>{y}</b>: %{{y}}<extra></extra>",
    ))
    fig = _apply_layout(fig, title, height)
    st.plotly_chart(fig, use_container_width=True)


def render_pie_chart(df, names, values, title="", colors=None, height=400):
    """
    Render an interactive pie/donut chart.

    Args:
        df: Pandas DataFrame.
        names: Column for slice labels.
        values: Column for slice sizes.
        title: Chart title.
        colors: List of colors for slices.
        height: Chart height.
    """
    colors = colors or COLOR_SEQUENCE[:len(df)]
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=df[names],
        values=df[values],
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#0F0F1A", width=2)),
        textfont=dict(size=13, color="#F1F5F9"),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>",
    ))
    fig = _apply_layout(fig, title, height)
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig, use_container_width=True)


def render_histogram(df, column, title="", color=None, nbins=30, height=400):
    """
    Render a histogram of a single column.

    Args:
        df: Pandas DataFrame.
        column: Column name for the histogram.
        title: Chart title.
        color: Bar color.
        nbins: Number of bins.
        height: Chart height.
    """
    color = color or COLORS["purple_light"]
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=df[column],
        nbinsx=nbins,
        marker=dict(
            color=color,
            line=dict(color="#0F0F1A", width=1),
        ),
        opacity=0.85,
        hovertemplate=f"<b>{column}</b>: %{{x}}<br>Count: %{{y}}<extra></extra>",
    ))
    fig = _apply_layout(fig, title, height)
    st.plotly_chart(fig, use_container_width=True)


def render_area_chart(df, x, y, title="", color=None, height=400):
    """
    Render a filled area chart.

    Args:
        df: Pandas DataFrame.
        x: Column name for x-axis.
        y: Column name for y-axis.
        title: Chart title.
        color: Area color.
        height: Chart height.
    """
    color = color or COLORS["cyan"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y],
        fill="tozeroy",
        mode="lines",
        line=dict(color=color, width=2, shape="spline"),
        fillcolor=f"rgba({_hex_to_rgb(color)}, 0.15)",
        hovertemplate=f"<b>{x}</b>: %{{x}}<br><b>{y}</b>: %{{y}}<extra></extra>",
    ))
    fig = _apply_layout(fig, title, height)
    st.plotly_chart(fig, use_container_width=True)


def render_heatmap(df, x, y, z, title="", height=450):
    """
    Render a heatmap chart.

    Args:
        df: Pandas DataFrame.
        x: Column for x-axis categories.
        y: Column for y-axis categories.
        z: Column for heat values.
        title: Chart title.
        height: Chart height.
    """
    pivot = df.pivot_table(values=z, index=y, columns=x, aggfunc="mean")
    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[
            [0.0, "#0F0F1A"],
            [0.25, "#1A1A2E"],
            [0.5, "#7C3AED"],
            [0.75, "#3B82F6"],
            [1.0, "#06B6D4"],
        ],
        hovertemplate="<b>%{x}</b>, <b>%{y}</b><br>Count: %{z}<extra></extra>",
        colorbar=dict(
            tickfont=dict(color="#94A3B8"),
            title=dict(text="Count", font=dict(color="#94A3B8")),
        ),
    ))
    fig = _apply_layout(fig, title, height)
    st.plotly_chart(fig, use_container_width=True)


def render_scatter_plot(df, x, y, title="", height=400):
    """
    Render a scatter plot with trend line.

    Args:
        df: Pandas DataFrame.
        x: Column for x-axis.
        y: Column for y-axis.
        title: Chart title.
        height: Chart height.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y],
        mode="markers",
        marker=dict(
            size=8,
            color=df[x],
            colorscale=[[0, "#3B82F6"], [0.5, "#7C3AED"], [1, "#EC4899"]],
            line=dict(width=1, color="#0F0F1A"),
            opacity=0.8,
        ),
        hovertemplate=f"<b>{x}</b>: %{{x}}<br><b>{y}</b>: %{{y:.1f}}%<extra></extra>",
    ))

    # Add trend line
    z = np.polyfit(df[x], df[y], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df[x].min(), df[x].max(), 100)
    fig.add_trace(go.Scatter(
        x=x_line, y=p(x_line),
        mode="lines",
        line=dict(color="#F59E0B", width=2, dash="dash"),
        name="Trend",
        showlegend=True,
    ))

    fig = _apply_layout(fig, title, height)
    st.plotly_chart(fig, use_container_width=True)


def render_density_map_plotly(density_array, title="Density Map"):
    """
    Render a density map array as a Plotly heatmap.

    Args:
        density_array: 2D numpy array of density values.
        title: Chart title.
    """
    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        z=density_array,
        colorscale=[
            [0.0, "#0F0F1A"],
            [0.2, "#1A1A2E"],
            [0.4, "#5B21B6"],
            [0.6, "#7C3AED"],
            [0.8, "#A78BFA"],
            [1.0, "#DDD6FE"],
        ],
        showscale=True,
        colorbar=dict(
            tickfont=dict(color="#94A3B8"),
            title=dict(text="Density", font=dict(color="#94A3B8")),
        ),
        hovertemplate="X: %{x}<br>Y: %{y}<br>Density: %{z:.3f}<extra></extra>",
    ))
    fig = _apply_layout(fig, title, 350)
    fig.update_layout(
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False, showgrid=False, autorange="reversed"),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_heatmap_overlay_plotly(heatmap_array, title="Heatmap Overlay"):
    """
    Render a heatmap overlay array as a Plotly heatmap.

    Args:
        heatmap_array: 2D numpy array of heatmap values.
        title: Chart title.
    """
    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        z=heatmap_array,
        colorscale=[
            [0.0, "#0F0F1A"],
            [0.2, "#16213E"],
            [0.4, "#10B981"],
            [0.6, "#F59E0B"],
            [0.8, "#F43F5E"],
            [1.0, "#FF0000"],
        ],
        showscale=True,
        colorbar=dict(
            tickfont=dict(color="#94A3B8"),
            title=dict(text="Intensity", font=dict(color="#94A3B8")),
        ),
        hovertemplate="X: %{x}<br>Y: %{y}<br>Intensity: %{z:.3f}<extra></extra>",
    ))
    fig = _apply_layout(fig, title, 350)
    fig.update_layout(
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False, showgrid=False, autorange="reversed"),
    )
    st.plotly_chart(fig, use_container_width=True)


def _hex_to_rgb(hex_color):
    """Convert hex color to comma-separated RGB string."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
    return f"{r}, {g}, {b}"
