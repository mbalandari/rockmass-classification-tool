"""
support.py
----------
Provides support recommendations based on Q-System value.
"""

from typing import Dict


def compute_support(q_value: float, span: float = 5.0) -> Dict[str, float]:
    """
    Compute support recommendations based on Q-System value.

    Args:
        q_value: Q-System classification value.
        span: Excavation span (m), used for bolt length estimation.

    Returns:
        Dictionary with:
            - category (str)
            - bolt_length (m)
            - bolt_spacing (m)
            - shotcrete_thickness (mm)
    """
    # Support category
    if q_value > 40:
        category = "No support required"
        bolt_spacing = 0.0
        shotcrete_thickness = 0.0
    elif q_value > 10:
        category = "Spot bolting"
        bolt_spacing = 2.5
        shotcrete_thickness = 0.0
    elif q_value > 4:
        category = "Systematic bolting"
        bolt_spacing = 2.0
        shotcrete_thickness = 0.0
    elif q_value > 1:
        category = "Bolting + mesh"
        bolt_spacing = 1.5
        shotcrete_thickness = 50.0
    elif q_value > 0.1:
        category = "Shotcrete + bolts"
        bolt_spacing = 1.5
        shotcrete_thickness = 75.0
    else:
        category = "Heavy support"
        bolt_spacing = 1.0
        shotcrete_thickness = 150.0

    # Bolt length (simple empirical relation)
    bolt_length = 2.0 + 0.15 * span

    return {
        "category": category,
        "bolt_length": bolt_length,
        "bolt_spacing": bolt_spacing,
        "shotcrete_thickness": shotcrete_thickness,
    }
