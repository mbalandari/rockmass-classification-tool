from dataclasses import dataclass


@dataclass
class RMRInput:
    ucs: float
    rqd: float
    joint_spacing: float
    joint_condition: str
    groundwater: str
    orientation: str


@dataclass
class QSystemInput:
    rqd: float
    jn: float
    jr: float
    ja: float
    jw: float
    srf: float


@dataclass
class GSIInput:
    structure: str
    surface_condition: str
    weathering: str


@dataclass
class ClassificationResult:
    rmr: float
    rmr_breakdown: dict
    q_value: float
    q_breakdown: dict
    gsi: float
    gsi_breakdown: dict
    support_recommendations: dict
