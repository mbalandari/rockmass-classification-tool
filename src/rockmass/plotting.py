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


def create_gsi_diagram(breakdown: dict):
    """
    Create a simple GSI diagram showing structure and surface adjustment.

    Args:
        breakdown: Dictionary with GSI components.

    Returns:
        Matplotlib Figure object.
    """
    fig, ax = plt.subplots(figsize=(6, 4))

    base = breakdown["structure_base"]
    adj = breakdown["surface_adjustment"]
    gsi = base + adj

    ax.bar(
        ["Base", "Adjustment", "Final GSI"],
        [base, adj, gsi],
        color=["#4C72B0", "#55A868", "#C44E52"],
    )

    ax.set_title("GSI Breakdown")
    ax.set_ylabel("GSI Value")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    fig.tight_layout()
    return fig
