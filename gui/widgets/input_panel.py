"""
Input panel for entering RMR, Q-System, and GSI parameters.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFormLayout,
    QLineEdit,
    QPushButton,
)


class InputPanel(QWidget):
    """Panel for user input parameters."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>Input Parameters</b>"))

        form = QFormLayout()

        # RMR inputs
        self.ucs = QLineEdit()
        self.rqd = QLineEdit()
        self.joint_spacing = QLineEdit()
        self.joint_condition = QLineEdit()
        self.groundwater = QLineEdit()
        self.orientation = QLineEdit()

        form.addRow("UCS (MPa):", self.ucs)
        form.addRow("RQD (%):", self.rqd)
        form.addRow("Joint Spacing (m):", self.joint_spacing)
        form.addRow("Joint Condition:", self.joint_condition)
        form.addRow("Groundwater:", self.groundwater)
        form.addRow("Orientation:", self.orientation)

        # Q-System inputs
        self.jn = QLineEdit()
        self.jr = QLineEdit()
        self.ja = QLineEdit()
        self.jw = QLineEdit()
        self.srf = QLineEdit()

        form.addRow("Jn:", self.jn)
        form.addRow("Jr:", self.jr)
        form.addRow("Ja:", self.ja)
        form.addRow("Jw:", self.jw)
        form.addRow("SRF:", self.srf)

        # GSI inputs
        self.structure = QLineEdit()
        self.surface_condition = QLineEdit()
        self.weathering = QLineEdit()

        form.addRow("Structure:", self.structure)
        form.addRow("Surface Condition:", self.surface_condition)
        form.addRow("Weathering:", self.weathering)

        layout.addLayout(form)

        # Run button
        self.run_button = QPushButton("Run Classification")
        layout.addWidget(self.run_button)

        self.setLayout(layout)
