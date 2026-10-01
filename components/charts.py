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




# def _create_visible_heatmap(data, palette):
#     """
#     Create a visually enhanced heatmap from the MCNN density output.

#     IMPORTANT:
#     This transformation is for visualization only.
#     The original density values and crowd count are never modified.
#     """
#     from PIL import Image, ImageFilter

#     arr = np.asarray(data, dtype=np.float32)
#     arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
#     arr = np.maximum(arr, 0.0)

#     # Compress the extremely large dynamic range.
#     arr = np.sqrt(arr)

#     # Normalize using the strongest density regions.
#     high = float(arr.max())

#     if high > 0:
#         arr = np.clip(arr / high, 0.0, 1.0)
#     else:
#         arr = np.zeros_like(arr)

#     # Convert to grayscale for controlled smoothing.
#     gray = (arr * 255.0).astype(np.uint8)
#     image = Image.fromarray(gray, mode="L")

#     # Spread sparse point detections into visible crowd regions.
#     image = image.filter(ImageFilter.GaussianBlur(radius=3.0))

#     arr = np.asarray(image, dtype=np.float32) / 255.0

#     # Re-normalize after smoothing.
#     if arr.max() > 0:
#         arr = arr / arr.max()

#     stops = np.linspace(0.0, 1.0, len(palette))
#     palette = np.asarray(palette, dtype=np.float32)

#     rgb = np.zeros((*arr.shape, 3), dtype=np.float32)

#     for channel in range(3):
#         rgb[..., channel] = np.interp(
#             arr,
#             stops,
#             palette[:, channel]
#         )

#     rgb = np.clip(rgb * 255.0, 0, 255).astype(np.uint8)

#     return Image.fromarray(rgb, mode="RGB")

def _create_visible_heatmap(data, palette):
    """
    Create a clearly visible heatmap from the MCNN density output.

    Visualization only:
    - Does not modify the original density map.
    - Does not modify the predicted crowd count.
    """

    from PIL import Image, ImageFilter

    arr = np.asarray(data, dtype=np.float32)
    arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
    arr = np.maximum(arr, 0.0)

    # If there is no density, return a completely black image.
    if arr.max() <= 0:
        return Image.fromarray(
            np.zeros((*arr.shape, 3), dtype=np.uint8),
            mode="RGB"
        )

    # ---------------------------------------------------------
    # 1. Focus normalization on NON-ZERO density values.
    # ---------------------------------------------------------
    nonzero = arr[arr > 0]

    if nonzero.size > 0:
        low = float(np.percentile(nonzero, 5))
        high = float(np.percentile(nonzero, 99))

        if high <= low:
            high = float(nonzero.max())

        arr = np.clip((arr - low) / max(high - low, 1e-8), 0.0, 1.0)

    # ---------------------------------------------------------
    # 2. Gamma correction makes weak density regions visible.
    # ---------------------------------------------------------
    arr = np.power(arr, 0.55)

    # ---------------------------------------------------------
    # 3. Smooth the sparse MCNN response.
    # ---------------------------------------------------------
    gray = (arr * 255.0).astype(np.uint8)

    image = Image.fromarray(gray, mode="L")
    image = image.filter(ImageFilter.GaussianBlur(radius=4.0))

    arr = np.asarray(image, dtype=np.float32) / 255.0

    # Normalize again after blur.
    if arr.max() > 0:
        arr = arr / arr.max()

    # ---------------------------------------------------------
    # 4. Convert normalized density to RGB heatmap.
    # ---------------------------------------------------------
    stops = np.linspace(0.0, 1.0, len(palette))
    palette = np.asarray(palette, dtype=np.float32)

    rgb = np.zeros((*arr.shape, 3), dtype=np.float32)

    for channel in range(3):
        rgb[..., channel] = np.interp(
            arr,
            stops,
            palette[:, channel]
        )

    rgb = np.clip(rgb * 255.0, 0, 255).astype(np.uint8)

    return Image.fromarray(rgb, mode="RGB")


def render_density_map_plotly(density_array, title="Density Map"):
    """
    Render the real MCNN density map as a rasterized heatmap.
    Visualization only — original density values are unchanged.
    """
    palette = [
        (0.03, 0.03, 0.08),
        (0.10, 0.06, 0.25),
        (0.25, 0.08, 0.55),
        (0.48, 0.15, 0.85),
        (0.70, 0.45, 1.00),
        (1.00, 0.95, 1.00),
    ]

    image = _create_visible_heatmap(density_array, palette)

    st.image(
        image,
        caption=title,
        use_container_width=True
    )


def render_heatmap_overlay_plotly(heatmap_array, title="Heatmap Overlay"):
    """
    Render the real MCNN density output as a visible intensity heatmap.
    Visualization only — original density values are unchanged.
    """
    palette = [
        (0.00, 0.05, 0.03),
        (0.00, 0.30, 0.20),
        (0.05, 0.75, 0.45),
        (1.00, 0.75, 0.00),
        (1.00, 0.25, 0.05),
        (1.00, 0.00, 0.00),
    ]

    image = _create_visible_heatmap(heatmap_array, palette)

    st.image(
        image,
        caption=title,
        use_container_width=True
    )


def _hex_to_rgb(hex_color):
    """Convert hex color to comma-separated RGB string."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
    return f"{r}, {g}, {b}"
