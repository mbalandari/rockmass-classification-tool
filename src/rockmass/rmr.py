"""
rmr.py
------
Functions for computing Rock Mass Rating (RMR) based on Bieniawski's system.
Each function returns a rating for a specific parameter.
"""

from typing import Dict
from .models import RMRInput


def strength_rating(ucs: float) -> int:
    """
    Return RMR strength rating based on UCS (MPa).

    Args:
        ucs: Uniaxial compressive strength in MPa.

    Returns:
        Integer rating for rock strength.
    """
    if ucs > 250:
        return 15
    elif ucs > 100:
        return 12
    elif ucs > 50:
        return 7
    elif ucs > 25:
        return 4
    elif ucs > 5:
        return 2
    else:
        return 0


def rqd_rating(rqd: float) -> int:
    """
    Return RMR rating based on RQD (%).

    Args:
        rqd: Rock Quality Designation in percent.

    Returns:
        Integer rating for RQD.
    """
    if rqd > 90:
        return 20
    elif rqd > 75:
        return 17
    elif rqd > 50:
        return 13
    elif rqd > 25:
        return 8
    else:
        return 3


def joint_spacing_rating(spacing: float) -> int:
    """
    Return RMR rating based on joint spacing (m).

    Args:
        spacing: Average joint spacing in meters.

    Returns:
        Integer rating for joint spacing.
    """
    if spacing > 2.0:
        return 20
    elif spacing > 0.6:
        return 15
    elif spacing > 0.2:
        return 10
    elif spacing > 0.06:
        return 8
    else:
        return 5


def joint_condition_rating(condition: str) -> int:
    """
    Return RMR rating based on joint condition category.

    Args:
        condition: Text category describing joint condition
                   (e.g. 'very_rough', 'rough', 'smooth', 'slickensided', 'soft_infill').

    Returns:
        Integer rating for joint condition.
    """
    mapping = {
        "very_rough": 30,
        "rough": 25,
        "slightly_rough": 25,
        "smooth": 20,
        "slickensided": 10,
        "soft_infill": 5,
        "very_soft_infill": 0,
    }
    return mapping.get(condition, 10)


def groundwater_rating(condition: str) -> int:
    """
    Return RMR rating based on groundwater condition.

    Args:
        condition: Text category ('dry', 'damp', 'wet', 'dripping', 'flowing').

    Returns:
        Integer rating for groundwater.
    """
    mapping = {
        "dry": 15,
        "damp": 10,
        "wet": 7,
        "dripping": 4,
        "flowing": 0,
    }
    return mapping.get(condition, 7)


def orientation_adjustment(orientation: str) -> int:
    """
    Return orientation adjustment for RMR.

    Args:
        orientation: Text category ('very_favorable', 'favorable', 'fair',
                                   'unfavorable', 'very_unfavorable').

    Returns:
        Integer adjustment (can be negative).
    """
    mapping = {
        "very_favorable": 5,
        "favorable": 2,
        "fair": 0,
        "unfavorable": -5,
        "very_unfavorable": -12,
    }
    return mapping.get(orientation, 0)


def compute_rmr(input_data: RMRInput) -> (float, Dict[str, float]):
    """
    Compute final RMR value and breakdown.

    Args:
        input_data: RMRInput object containing all required parameters.

    Returns:
        Tuple of:
            - RMR value (float)
            - breakdown dict with component ratings.
    """
    r1 = strength_rating(input_data.ucs)
    r2 = rqd_rating(input_data.rqd)
    r3 = joint_spacing_rating(input_data.joint_spacing)
    r4 = joint_condition_rating(input_data.joint_condition)
    r5 = groundwater_rating(input_data.groundwater)
    r6 = orientation_adjustment(input_data.orientation)

    rmr_value = r1 + r2 + r3 + r4 + r5 + r6

    breakdown = {
        "strength": r1,
        "rqd": r2,
        "joint_spacing": r3,
        "joint_condition": r4,
        "groundwater": r5,
        "orientation": r6,
    }

    return float(rmr_value), breakdown
