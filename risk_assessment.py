"""
============================================================
Crowd Risk Assessment Module
============================================================
Uses the density level already calculated by the trained
MCNN model.

Model levels:
    Low       -> Safe
    Medium    -> Monitor
    High      -> Alert
    Very High -> Critical Alert
============================================================
"""


def assess_crowd_risk(density_level):
    """
    Convert the model's existing density level into a
    dashboard alert state.

    No new crowd-count thresholds are introduced here.
    """

    level = str(density_level).strip().lower()

    if level == "very high":
        return {
            "level": "CRITICAL",
            "title": "Critical Crowd Density",
            "message": (
                "Very high crowd density has been detected. "
                "Immediate attention is recommended."
            ),
            "emoji": "🚨",
        }

    elif level == "high":
        return {
            "level": "DANGER",
            "title": "High Crowd Density Alert",
            "message": (
                "High crowd density has been detected. "
                "The monitoring team should check the area."
            ),
            "emoji": "⚠️",
        }

    elif level == "medium":
        return {
            "level": "WARNING",
            "title": "Crowd Density Warning",
            "message": (
                "Medium crowd density has been detected. "
                "Continue monitoring the area."
            ),
            "emoji": "⚠️",
        }

    else:
        return {
            "level": "SAFE",
            "title": "Crowd Density Normal",
            "message": (
                "Crowd density is currently within the normal range."
            ),
            "emoji": "✓",
        }