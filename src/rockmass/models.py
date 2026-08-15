from dataclasses import dataclass
from typing import Dict


@dataclass
class RMRInput:
    """Input parameters for RMR classification."""

    ucs: float
    rqd: float
    joint_spacing: float
    joint_condition: str
    groundwater: str
    orientation: str


@dataclass
class QSystemInput:
    """Input parameters for Q-System classification."""

    rqd: float
    jn: float
    jr: float
    ja: float
    jw: float
    srf: float


@dataclass
class GSIInput:
    """Input parameters for GSI estimation."""

    structure: str
    surface_condition: str
    weathering: str


@dataclass
class ClassificationResult:
    """
    Combined classification result for RMR, Q-System, and GSI.

    Attributes:
        rmr: Final RMR value.
        rmr_breakdown: Detailed RMR component ratings.
        q_value: Final Q-System value.
        q_breakdown: Detailed Q-System components.
        gsi: Final GSI value.
        gsi_breakdown: Detailed GSI components.
        support_recommendations: Recommended support measures.
    """

    rmr: float
    rmr_breakdown: Dict[str, float]
    q_value: float
    q_breakdown: Dict[str, float]
    gsi: float
    gsi_breakdown: Dict[str, float]
    support_recommendations: Dict[str, float]
