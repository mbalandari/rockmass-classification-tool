"""
qsystem.py
----------
Implements NGI Q-System classification.
Q = (RQD / Jn) * (Jr / Ja) * (Jw / SRF)
"""

from typing import Dict
from .models import QSystemInput


def compute_q(input_data: QSystemInput) -> (float, Dict[str, float]):
    """
    Compute Q-System value and breakdown.

    Args:
        input_data: QSystemInput object with RQD, Jn, Jr, Ja, Jw, SRF.

    Returns:
        Tuple of:
            - Q value (float)
            - breakdown dict with each component.
    """
    # Avoid division by zero
    jn = max(input_data.jn, 0.1)
    ja = max(input_data.ja, 0.1)
    srf = max(input_data.srf, 0.1)

    term1 = input_data.rqd / jn
    term2 = input_data.jr / ja
    term3 = input_data.jw / srf

    q_value = term1 * term2 * term3

    breakdown = {
        "RQD_over_Jn": term1,
        "Jr_over_Ja": term2,
        "Jw_over_SRF": term3,
        "RQD": input_data.rqd,
        "Jn": input_data.jn,
        "Jr": input_data.jr,
        "Ja": input_data.ja,
        "Jw": input_data.jw,
        "SRF": input_data.srf,
    }

    return float(q_value), breakdown
