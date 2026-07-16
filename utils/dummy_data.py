"""
============================================================
Enhanced MCNN Crowd Density Dashboard — Dummy Data Module
============================================================
Provides all static/dummy data for the frontend prototype.
All functions return realistic-looking data without any
backend or ML model dependencies.
============================================================
"""

import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ============================================================
# 1. PROJECT INFORMATION
# ============================================================

PROJECT_INFO = {
    "title": "Enhanced Multi-Column Convolutional Neural Networks (MCNN)",
    "subtitle": "for Accurate Crowd Density Estimation with Adaptive Collation",
    "short_title": "Enhanced MCNN Crowd Density Estimation",
    "version": "v2.1.0",
    "year": "2025-2026",
    "department": "Computer Engineering",
    "institution": "XYZ College of Engineering",
    "university": "University of Mumbai",
}

PROJECT_OVERVIEW = (
    "This project presents an Enhanced Multi-Column Convolutional Neural Network "
    "(MCNN) architecture for accurate crowd density estimation. By leveraging three "
    "parallel CNN columns with different receptive field sizes, the model captures "
    "multi-scale features from crowd images. An innovative Adaptive Collation "
    "mechanism dynamically fuses the outputs of these columns, producing highly "
    "accurate density maps that enable precise crowd counting across diverse scenes "
    "— from sparse gatherings to extremely dense events."
)

RESEARCH_MOTIVATION = (
    "Crowd density estimation is critical for public safety, urban planning, and "
    "event management. Traditional single-column CNN approaches struggle with "
    "large variations in head sizes caused by perspective distortion. Our Enhanced "
    "MCNN overcomes this limitation by processing the input image through multiple "
    "columns at different scales, capturing both small, distant heads and large, "
    "nearby ones. The Adaptive Collation layer intelligently weighs each column's "
    "contribution based on local crowd characteristics, significantly improving "
    "estimation accuracy over state-of-the-art methods."
)

PROBLEM_STATEMENT = (
    "Estimating crowd density in images and videos with high accuracy remains a "
    "challenging computer vision problem due to severe occlusion, perspective "
    "distortion, non-uniform density distributions, and varying illumination "
    "conditions. Existing methods often fail to generalize across different "
    "crowd scenes and densities. This project addresses these challenges by "
    "developing an Enhanced MCNN with Adaptive Collation that achieves superior "
    "accuracy and robustness across diverse crowd scenarios."
)

METHODOLOGY = (
    "The proposed methodology involves: (1) Data collection and preprocessing of "
    "crowd images from benchmark datasets (ShanghaiTech, UCF_CC_50, etc.), "
    "(2) Ground truth density map generation using Gaussian kernel-based head "
    "annotations, (3) Design and implementation of the Enhanced MCNN architecture "
    "with three parallel CNN columns (small, medium, large receptive fields), "
    "(4) Implementation of the Adaptive Collation layer for intelligent feature "
    "fusion, (5) Training with a composite loss function combining MSE and SSIM, "
    "and (6) Evaluation using MAE, MSE, and PSNR metrics on benchmark datasets."
)


# ============================================================
# 2. OBJECTIVES
# ============================================================

OBJECTIVES = [
    {
        "icon": "🎯",
        "title": "Accurate Crowd Counting",
        "desc": "Develop a deep learning model that accurately estimates crowd "
                "counts from single images with minimal mean absolute error.",
    },
    {
        "icon": "🏗️",
        "title": "Multi-Scale Feature Extraction",
        "desc": "Design a multi-column CNN architecture that captures features "
                "at multiple spatial scales to handle perspective distortion.",
    },
    {
        "icon": "🔗",
        "title": "Adaptive Feature Fusion",
        "desc": "Implement an adaptive collation mechanism that dynamically "
                "fuses multi-column outputs based on local crowd characteristics.",
    },
    {
        "icon": "🗺️",
        "title": "High-Quality Density Maps",
        "desc": "Generate accurate pixel-level crowd density maps that "
                "visualize crowd distribution across the entire image.",
    },
    {
        "icon": "⚡",
        "title": "Real-Time Inference",
        "desc": "Optimize the model for fast inference suitable for real-time "
                "crowd monitoring and surveillance applications.",
    },
    {
        "icon": "📊",
        "title": "Benchmark Evaluation",
        "desc": "Evaluate the model against state-of-the-art methods on "
                "standard benchmark datasets to demonstrate superiority.",
    },
]


# ============================================================
# 3. HERO STATISTICS (Animated Counters)
# ============================================================

HERO_STATS = [
    {
        "icon": "🎯",
        "value": "95.6%",
        "label": "Accuracy",
        "color": "purple",
    },
    {
        "icon": "🖼️",
        "value": "5,000+",
        "label": "Images Processed",
        "color": "blue",
    },
    {
        "icon": "⚡",
        "value": "120 FPS",
        "label": "Processing Speed",
        "color": "emerald",
    },
    {
        "icon": "🧠",
        "value": "3",
        "label": "CNN Columns",
        "color": "amber",
    },
]


# ============================================================
# 4. TECHNOLOGY STACK
# ============================================================

TECH_STACK = [
    {"icon": "🐍", "name": "Python 3.10", "desc": "Core Language"},
    {"icon": "🔥", "name": "PyTorch", "desc": "Deep Learning"},
    {"icon": "📊", "name": "Streamlit", "desc": "Web Dashboard"},
    {"icon": "👁️", "name": "OpenCV", "desc": "Image Processing"},
    {"icon": "📈", "name": "Plotly", "desc": "Visualizations"},
    {"icon": "🔢", "name": "NumPy", "desc": "Numerical Computing"},
    {"icon": "🐼", "name": "Pandas", "desc": "Data Analysis"},
    {"icon": "🖼️", "name": "Pillow", "desc": "Image Handling"},
]


# ============================================================
# 5. FEATURES
# ============================================================

FEATURES = [
    {
        "icon": "🧠",
        "title": "Enhanced MCNN Architecture",
        "desc": "Three parallel CNN columns with different filter sizes "
                "capture multi-scale crowd features simultaneously.",
    },
    {
        "icon": "🔗",
        "title": "Adaptive Collation",
        "desc": "Intelligent feature fusion mechanism that dynamically weighs "
                "column outputs based on local crowd density patterns.",
    },
    {
        "icon": "🗺️",
        "title": "Density Map Generation",
        "desc": "Produces high-quality pixel-level density maps that visualize "
                "crowd distribution with fine spatial granularity.",
    },
    {
        "icon": "⚡",
        "title": "Real-Time Processing",
        "desc": "Optimized architecture achieves 120 FPS inference speed, "
                "enabling live crowd monitoring applications.",
    },
    {
        "icon": "📊",
        "title": "Interactive Analytics",
        "desc": "Comprehensive dashboard with charts, KPIs, and trend analysis "
                "for crowd management insights.",
    },
    {
        "icon": "🎨",
        "title": "Heatmap Visualization",
        "desc": "Beautiful heatmap overlays on crowd images showing density "
                "concentrations with intuitive color gradients.",
    },
]


# ============================================================
# 6. WORKFLOW STEPS (Timeline)
# ============================================================

WORKFLOW_STEPS = [
    {
        "step": 1,
        "title": "Image Acquisition",
        "desc": "Capture or upload crowd images from cameras, drones, "
                "or surveillance feeds.",
    },
    {
        "step": 2,
        "title": "Preprocessing",
        "desc": "Resize, normalize, and augment images for optimal "
                "model input preparation.",
    },
    {
        "step": 3,
        "title": "Multi-Column Feature Extraction",
        "desc": "Process through 3 parallel CNN columns with 3×3, 5×5, "
                "and 7×7 filters to capture multi-scale features.",
    },
    {
        "step": 4,
        "title": "Adaptive Collation",
        "desc": "Dynamically fuse column outputs using learned attention "
                "weights for optimal feature combination.",
    },
    {
        "step": 5,
        "title": "Density Map Generation",
        "desc": "Generate pixel-level density map predicting crowd "
                "distribution across the entire image.",
    },
    {
        "step": 6,
        "title": "Crowd Count & Analysis",
        "desc": "Integrate the density map to obtain total crowd count "
                "and generate analytics insights.",
    },
]


# ============================================================
# 7. PREDICTION SIMULATION
# ============================================================

# Processing pipeline steps for the prediction page animation
PROCESSING_STEPS = [
    {"icon": "📤", "text": "Uploading Image...", "duration": 0.8},
    {"icon": "🔧", "text": "Preprocessing Image...", "duration": 1.0},
    {"icon": "🧠", "text": "Running Enhanced MCNN...", "duration": 2.0},
    {"icon": "🗺️", "text": "Generating Density Map...", "duration": 1.2},
    {"icon": "🔢", "text": "Calculating Crowd Count...", "duration": 0.8},
    {"icon": "✅", "text": "Prediction Complete!", "duration": 0.5},
]


def get_prediction_results():
    """
    Generate slightly randomized prediction results.
    Called each time a prediction is simulated.
    Returns a dict with crowd count, confidence, inference time, etc.
    """
    crowd_count = random.randint(210, 350)
    confidence = round(random.uniform(93.0, 98.5), 1)
    inference_time = round(random.uniform(0.35, 0.55), 2)

    # Determine density level based on crowd count
    if crowd_count < 50:
        density_level = "Low"
        density_class = "density-low"
    elif crowd_count < 150:
        density_level = "Medium"
        density_class = "density-medium"
    elif crowd_count < 300:
        density_level = "High"
        density_class = "density-high"
    else:
        density_level = "Very High"
        density_class = "density-very-high"

    return {
        "crowd_count": crowd_count,
        "confidence": confidence,
        "inference_time": inference_time,
        "density_level": density_level,
        "density_class": density_class,
        "model_version": "Enhanced MCNN v2.1",
        "input_resolution": "1024 × 768",
        "density_map_resolution": "256 × 192",
    }


# ============================================================
# 8. ANALYTICS DATA GENERATORS
# ============================================================

def get_daily_predictions(days=30):
    """Generate simulated daily prediction data for the past N days."""
    dates = [
        (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(days - 1, -1, -1)
    ]
    counts = [random.randint(80, 450) for _ in dates]
    confidence_scores = [round(random.uniform(90.0, 99.0), 1) for _ in dates]
    inference_times = [round(random.uniform(0.30, 0.60), 2) for _ in dates]

    return pd.DataFrame({
        "Date": dates,
        "Crowd Count": counts,
        "Confidence (%)": confidence_scores,
        "Inference Time (s)": inference_times,
    })


def get_weekly_predictions(weeks=12):
    """Generate simulated weekly aggregate prediction data."""
    week_labels = [f"Week {i + 1}" for i in range(weeks)]
    avg_counts = [random.randint(150, 380) for _ in week_labels]
    total_predictions = [random.randint(20, 60) for _ in week_labels]

    return pd.DataFrame({
        "Week": week_labels,
        "Avg Crowd Count": avg_counts,
        "Total Predictions": total_predictions,
    })


def get_monthly_predictions(months=6):
    """Generate simulated monthly aggregate prediction data."""
    month_names = ["January", "February", "March", "April", "May", "June"][:months]
    avg_counts = [random.randint(180, 350) for _ in month_names]
    total_predictions = [random.randint(80, 250) for _ in month_names]
    avg_confidence = [round(random.uniform(92.0, 97.5), 1) for _ in month_names]

    return pd.DataFrame({
        "Month": month_names,
        "Avg Crowd Count": avg_counts,
        "Total Predictions": total_predictions,
        "Avg Confidence (%)": avg_confidence,
    })


def get_density_distribution():
    """Generate density level distribution for pie chart."""
    return pd.DataFrame({
        "Density Level": ["Low", "Medium", "High", "Very High"],
        "Count": [
            random.randint(30, 60),
            random.randint(80, 150),
            random.randint(100, 180),
            random.randint(20, 50),
        ],
        "Color": ["#10B981", "#3B82F6", "#F59E0B", "#F43F5E"],
    })


def get_crowd_count_histogram(n=200):
    """Generate crowd count values for histogram distribution."""
    # Simulating a right-skewed distribution (common in crowd data)
    counts = np.concatenate([
        np.random.normal(100, 40, n // 3),
        np.random.normal(250, 60, n // 3),
        np.random.normal(400, 80, n // 3),
    ])
    counts = np.clip(counts, 10, 600).astype(int)
    return pd.DataFrame({"Crowd Count": counts})


def get_hourly_heatmap_data():
    """Generate hourly crowd density data for heatmap (7 days × 24 hours)."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"]
    hours = list(range(24))

    data = []
    for day in days:
        for hour in hours:
            # Simulate higher counts during peak hours
            if 9 <= hour <= 18:
                base = random.randint(150, 400)
            elif 7 <= hour <= 9 or 18 <= hour <= 21:
                base = random.randint(80, 250)
            else:
                base = random.randint(10, 100)

            # Weekends generally higher
            if day in ("Saturday", "Sunday"):
                base = int(base * 1.3)

            data.append({"Day": day, "Hour": hour, "Count": base})

    return pd.DataFrame(data)


def get_scatter_data(n=100):
    """Generate crowd count vs confidence scatter plot data."""
    counts = np.random.randint(20, 500, n)
    # Confidence tends to decrease slightly with very high counts
    confidence = np.clip(
        98 - (counts / 500) * 8 + np.random.normal(0, 2, n),
        85, 99.5
    )
    return pd.DataFrame({
        "Crowd Count": counts,
        "Confidence (%)": np.round(confidence, 1),
    })


def get_kpi_summary():
    """Generate KPI summary values for the analytics dashboard."""
    return {
        "total_predictions": random.randint(1200, 2500),
        "avg_crowd_count": random.randint(180, 280),
        "min_count": random.randint(12, 35),
        "max_count": random.randint(450, 620),
        "avg_confidence": round(random.uniform(94.0, 97.5), 1),
        "avg_inference_time": round(random.uniform(0.38, 0.48), 2),
        "total_images": random.randint(4500, 6000),
        "uptime": "99.9%",
    }


# ============================================================
# 9. MODEL ARCHITECTURE DETAILS
# ============================================================

MCNN_ARCHITECTURE = {
    "overview": (
        "The Enhanced MCNN consists of three parallel CNN columns, each "
        "designed to extract features at a different spatial scale. Column A "
        "uses small 3×3 filters for fine-grained local features, Column B "
        "uses 5×5 filters for medium-scale patterns, and Column C uses 7×7 "
        "filters for large-scale contextual information. The Adaptive "
        "Collation layer then intelligently fuses these multi-scale features."
    ),
    "columns": [
        {
            "name": "Column A — Fine Scale",
            "filter": "3×3 Conv",
            "icon": "🔬",
            "desc": "Captures small, fine-grained features such as "
                    "individual heads in close proximity. Best for "
                    "detecting nearby, large-appearing pedestrians.",
            "layers": "Conv(3×3) → BN → ReLU → Pool → Conv(3×3) → BN → ReLU",
        },
        {
            "name": "Column B — Medium Scale",
            "filter": "5×5 Conv",
            "icon": "📐",
            "desc": "Extracts medium-scale patterns capturing small groups "
                    "and moderate density regions. Balances detail and context.",
            "layers": "Conv(5×5) → BN → ReLU → Pool → Conv(5×5) → BN → ReLU",
        },
        {
            "name": "Column C — Coarse Scale",
            "filter": "7×7 Conv",
            "icon": "🔭",
            "desc": "Processes large receptive fields for global context, "
                    "capturing distant, small-appearing heads and overall "
                    "crowd structure patterns.",
            "layers": "Conv(7×7) → BN → ReLU → Pool → Conv(7×7) → BN → ReLU",
        },
    ],
    "collation": (
        "The Adaptive Collation layer uses a learned attention mechanism "
        "to dynamically weight each column's feature maps. Unlike simple "
        "averaging or concatenation, this approach assigns spatially-varying "
        "weights, allowing the model to emphasize fine-scale features in "
        "dense regions and coarse-scale features in sparse regions."
    ),
    "density_map": (
        "The fused feature maps are passed through a 1×1 convolution layer "
        "to produce a single-channel density map. Each pixel value represents "
        "the estimated crowd density at that location. Integrating (summing) "
        "all pixel values yields the total estimated crowd count."
    ),
}

ADVANTAGES = [
    {"icon": "✅", "title": "Multi-Scale Robustness",
     "desc": "Handles extreme perspective variations and diverse head sizes."},
    {"icon": "✅", "title": "Adaptive Fusion",
     "desc": "Dynamically adjusts feature importance based on local density."},
    {"icon": "✅", "title": "High Accuracy",
     "desc": "Achieves state-of-the-art MAE on benchmark datasets."},
    {"icon": "✅", "title": "Fast Inference",
     "desc": "Optimized for real-time processing at 120+ FPS."},
    {"icon": "✅", "title": "Generalization",
     "desc": "Performs well across indoor, outdoor, and aerial crowd scenes."},
    {"icon": "✅", "title": "End-to-End Training",
     "desc": "Fully differentiable architecture trained end-to-end."},
]

APPLICATIONS = [
    {"icon": "🏟️", "title": "Event Management",
     "desc": "Real-time crowd monitoring at concerts, sports, and festivals."},
    {"icon": "🚇", "title": "Public Transport",
     "desc": "Station and platform crowd density monitoring for safety."},
    {"icon": "🏙️", "title": "Smart Cities",
     "desc": "Urban planning and pedestrian flow analysis."},
    {"icon": "🛡️", "title": "Security & Surveillance",
     "desc": "Anomaly detection and crowd safety monitoring."},
    {"icon": "🏥", "title": "Healthcare",
     "desc": "Hospital and clinic crowd management systems."},
    {"icon": "🛒", "title": "Retail Analytics",
     "desc": "Store foot traffic analysis and customer flow optimization."},
]

FUTURE_IMPROVEMENTS = [
    {"icon": "🎥", "title": "Video Stream Processing",
     "desc": "Extend to real-time video stream analysis with temporal tracking."},
    {"icon": "🌐", "title": "Edge Deployment",
     "desc": "Model compression for deployment on edge devices and IoT."},
    {"icon": "🧩", "title": "Attention Mechanisms",
     "desc": "Integrate self-attention and transformer blocks for better context."},
    {"icon": "📱", "title": "Mobile Application",
     "desc": "Cross-platform mobile app for on-the-go crowd monitoring."},
    {"icon": "☁️", "title": "Cloud Integration",
     "desc": "Scalable cloud-based API for enterprise crowd analytics."},
    {"icon": "🤖", "title": "Anomaly Detection",
     "desc": "Detect unusual crowd behaviors like stampedes or surges."},
]


# ============================================================
# 10. TEAM MEMBERS
# ============================================================

TEAM_MEMBERS = [
    {
        "name": "Sejal Gupta",
        "role": "Developer & Researcher",
        "avatar": "👩‍💻",
        "bio": "Focused on model architecture design, training pipeline, "
               "and performance optimization of the Enhanced MCNN.",
    },
    {
        "name": "Riddhi Ghosalkar",
        "role": "Developer & Researcher",
        "avatar": "👩‍🔬",
        "bio": "Specialized in data preprocessing, density map generation, "
               "and benchmark evaluation methodologies.",
    },
    {
        "name": "Kanika Bhuvad",
        "role": "Developer & Researcher",
        "avatar": "👩‍🎓",
        "bio": "Responsible for dashboard development, visualization design, "
               "and user interface implementation.",
    },
]

GUIDE_INFO = {
    "name": "Prof. [Guide Name]",
    "role": "Project Guide",
    "avatar": "👨‍🏫",
    "department": "Department of Computer Engineering",
    "institution": PROJECT_INFO["institution"],
}


# ============================================================
# 11. ABOUT PAGE DATA
# ============================================================

EXPECTED_OUTCOMES = [
    "An Enhanced MCNN model achieving MAE < 65 on ShanghaiTech Part A dataset.",
    "High-quality density maps with PSNR > 25 dB.",
    "Real-time inference capability at 120+ FPS on GPU hardware.",
    "A user-friendly web dashboard for crowd density visualization.",
    "Comprehensive evaluation against CSRNet, SANet, and MCNN baselines.",
]

FUTURE_SCOPE = [
    "Integration with live video surveillance systems for real-time monitoring.",
    "Deployment on edge computing devices (NVIDIA Jetson, Raspberry Pi).",
    "Extension to 3D crowd density estimation using depth information.",
    "Multi-camera crowd counting for large-scale venue management.",
    "Transfer learning for domain-specific crowd types (vehicles, wildlife).",
]

PROJECT_FEATURES = [
    {"icon": "📤", "title": "Image Upload", "desc": "Drag-and-drop crowd image upload"},
    {"icon": "🧠", "title": "AI Prediction", "desc": "Enhanced MCNN-based estimation"},
    {"icon": "🗺️", "title": "Density Maps", "desc": "Pixel-level density visualization"},
    {"icon": "🌡️", "title": "Heatmaps", "desc": "Intuitive heat-based overlays"},
    {"icon": "📊", "title": "Analytics", "desc": "Charts, KPIs, and trend analysis"},
    {"icon": "📈", "title": "History", "desc": "Track prediction trends over time"},
    {"icon": "📥", "title": "Export", "desc": "Download reports and results"},
    {"icon": "🎨", "title": "Premium UI", "desc": "Modern, responsive dark theme"},
]

REFERENCES = [
    "Zhang, Y., et al. 'Single-Image Crowd Counting via Multi-Column "
    "Convolutional Neural Network.' CVPR 2016.",
    "Li, Y., et al. 'CSRNet: Dilated Convolutional Neural Networks for "
    "Understanding the Highly Congested Scenes.' CVPR 2018.",
    "Cao, X., et al. 'Scale Aggregation Network for Accurate and Efficient "
    "Crowd Counting.' ECCV 2018.",
    "Liu, W., et al. 'Context-Aware Crowd Counting.' CVPR 2019.",
    "Wang, Q., et al. 'NASCount: Counting-by-Density with Neural Architecture "
    "Search.' ECCV 2020.",
]

ACKNOWLEDGEMENTS = (
    "We express our sincere gratitude to our project guide for their invaluable "
    "guidance and constant encouragement throughout this project. We also thank "
    "the Department of Computer Engineering and our institution for providing the "
    "necessary resources and infrastructure. Special thanks to the authors of the "
    "ShanghaiTech and UCF_CC_50 datasets for making their data publicly available "
    "for research purposes."
)


# ============================================================
# 12. DENSITY MAP & HEATMAP GENERATORS (Placeholder Images)
# ============================================================

def generate_dummy_density_map(width=256, height=192):
    """
    Generate a dummy density map as a NumPy array.
    Creates a random blob-like pattern simulating crowd density.
    Returns an array suitable for Plotly heatmap visualization.
    """
    # Create random density blobs
    density = np.zeros((height, width), dtype=np.float32)

    # Add multiple Gaussian blobs
    num_blobs = random.randint(5, 12)
    for _ in range(num_blobs):
        cx = random.randint(20, width - 20)
        cy = random.randint(20, height - 20)
        sigma_x = random.randint(15, 50)
        sigma_y = random.randint(15, 50)
        amplitude = random.uniform(0.5, 1.0)

        y, x = np.ogrid[:height, :width]
        blob = amplitude * np.exp(
            -((x - cx) ** 2 / (2 * sigma_x ** 2)
              + (y - cy) ** 2 / (2 * sigma_y ** 2))
        )
        density += blob

    # Normalize to [0, 1]
    if density.max() > 0:
        density = density / density.max()

    return density


def generate_dummy_heatmap(width=256, height=192):
    """
    Generate a dummy heatmap overlay as a NumPy array.
    Similar to density map but with more diffused patterns.
    Returns an array suitable for Plotly visualization.
    """
    heatmap = np.zeros((height, width), dtype=np.float32)

    # More spread-out blobs for heatmap
    num_regions = random.randint(3, 8)
    for _ in range(num_regions):
        cx = random.randint(30, width - 30)
        cy = random.randint(30, height - 30)
        sigma = random.randint(30, 80)
        amplitude = random.uniform(0.3, 1.0)

        y, x = np.ogrid[:height, :width]
        region = amplitude * np.exp(
            -((x - cx) ** 2 + (y - cy) ** 2) / (2 * sigma ** 2)
        )
        heatmap += region

    # Normalize
    if heatmap.max() > 0:
        heatmap = heatmap / heatmap.max()

    return heatmap
