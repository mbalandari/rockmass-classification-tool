"""
gsi.py
------
Implements Hoek–Marinos GSI estimation using simple lookup tables
for structure and surface condition.
"""

from typing import Dict
from .models import GSIInput


def structure_base(structure: str) -> int:
    """
    Return base GSI range midpoint for a given structure class.

    Args:
        structure: Text category ('massive', 'blocky', 'very_blocky',
                                  'disintegrated', 'laminated', 'sheared').

    Returns:
        Integer base GSI value.
    """
    mapping = {
        "massive": 82,  # midpoint of 75–90
        "blocky": 70,  # 65–75
        "very_blocky": 60,  # 55–65
        "disintegrated": 38,  # 30–45
        "laminated": 30,  # 25–35
        "sheared": 18,  # 10–25
    }
    return mapping.get(structure, 50)


def surface_adjustment(surface_condition: str) -> int:
    """
    Return GSI adjustment based on surface condition.

    Args:
        surface_condition: Text category ('fresh', 'slightly_weathered',
                                         'moderately_weathered', 'highly_weathered').

    Returns:
        Integer adjustment (can be negative).
    """
    mapping = {
        "fresh": 5,
        "slightly_weathered": 0,
        "moderately_weathered": -5,
        "highly_weathered": -10,
    }
    return mapping.get(surface_condition, 0)


def compute_gsi(input_data: GSIInput) -> (float, Dict[str, float]):
    """
    Compute GSI value and breakdown.

    Args:
        input_data: GSIInput object with structure, surface condition, weathering.

    Returns:
        Tuple of:
            - GSI value (float)
            - breakdown dict with components.
    """
    base = structure_base(input_data.structure)
    adj = surface_adjustment(input_data.surface_condition)

    gsi_value = base + adj

    breakdown = {
        "structure_base": base,
        "surface_adjustment": adj,
        "weathering": input_data.weathering,
    }

    return float(gsi_value), breakdown
