"""
plotting.py
-----------
Generates engineering-grade charts for RMR, Q-System, and GSI.
Used in GUI and report generation.
"""

import matplotlib.pyplot as plt
import numpy as np


def create_rmr_bar_chart(breakdown: dict):
    """
    Create a bar chart showing RMR component ratings.

    Args:
        breakdown: Dictionary with RMR component ratings.

    Returns:
        Matplotlib Figure object.
    """
    labels = list(breakdown.keys())
    values = list(breakdown.values())

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, values, color="#4C72B0")

    ax.set_title("RMR Breakdown")
    ax.set_ylabel("Rating")
    ax.set_ylim(0, max(values) + 5)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    fig.tight_layout()
    return fig


def create_q_radar_chart(breakdown: dict):
    """
    Create a radar chart for Q-System components.

    Args:
        breakdown: Dictionary with Q-System components.

    Returns:
        Matplotlib Figure object.
    """
    labels = ["RQD/Jn", "Jr/Ja", "Jw/SRF"]
    values = [
        breakdown["RQD_over_Jn"],
        breakdown["Jr_over_Ja"],
        breakdown["Jw_over_SRF"],
    ]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, "o-", linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title("Q-System Radar Chart")

    fig.tight_layout()
    return fig


def create_gsi_diagram(gsi_breakdown, gsi_value=None):
    """
    Creates a real GSI diagram with structure domains and a marker for the
    calculated GSI value.

    gsi_breakdown: dict (not used for value, only kept for future extensions)
    gsi_value: numeric GSI (if None, try to infer from breakdown)
    """

    import matplotlib.pyplot as plt

    # If gsi_value is not provided, try to infer it from the dict
    if gsi_value is None:
        # Try common key names
        for key in ("GSI", "gsi", "value"):
            if key in gsi_breakdown:
                gsi_value = gsi_breakdown[key]
                break
        else:
            # As a last resort, if the dict is empty or doesn’t contain GSI,
            # fall back to 0
            gsi_value = 0

    fig, ax = plt.subplots(figsize=(6, 4))

    # GSI zones (Hoek & Marinos)
    zones = [
        ("Massive", 75, 100, "#4C72B0"),
        ("Blocky", 55, 75, "#55A868"),
        ("Very Blocky", 35, 55, "#C44E52"),
        ("Disintegrated", 20, 35, "#8172B2"),
        ("Laminated", 10, 20, "#CCB974"),
        ("Sheared", 0, 10, "#64B5CD"),
    ]

    # Draw shaded zones
    for label, gsi_min, gsi_max, color in zones:
        ax.fill_between(
            [0, 1],
            gsi_min,
            gsi_max,
            color=color,
            alpha=0.5,
            label=f"{label} ({gsi_min}-{gsi_max})",
        )

    # Plot the user's GSI value
    ax.plot(0.5, gsi_value, "ko", markersize=10)
    ax.text(0.52, gsi_value, f"GSI = {gsi_value}", va="center")

    # Formatting
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 100)
    ax.set_xticks([])
    ax.set_ylabel("Geological Strength Index (GSI)")
    ax.set_title("GSI Structure Domains (Hoek & Marinos)")

    ax.legend(loc="lower right", fontsize=8)

    fig.tight_layout()
    return fig


def save_figure_as_png(fig, filename):
    """Save a Matplotlib figure as a PNG file."""
    fig.savefig(filename, dpi=300, bbox_inches="tight")
