"""
qsystem.py
----------
Implements NGI Q-System classification.
Includes rating tables for Jn, Jr, Ja, Jw, SRF and the Q formula.
"""


def compute_q(input: QSystemInput) -> (float, dict):
    """
    Compute Q-System value and breakdown.
    Q = (RQD / Jn) * (Jr / Ja) * (Jw / SRF)
    """
    ...
