"""
Panel for displaying classification results.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ResultPanel(QWidget):
    """Displays RMR, Q-System, GSI, and support results."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>Results</b>"))

        self.rmr_label = QLabel("RMR: -")
        self.q_label = QLabel("Q-System: -")
        self.gsi_label = QLabel("GSI: -")
        self.support_label = QLabel("Support: -")

        layout.addWidget(self.rmr_label)
        layout.addWidget(self.q_label)
        layout.addWidget(self.gsi_label)
        layout.addWidget(self.support_label)

        self.setLayout(layout)

    def update_results(self, results):
        """Update displayed results."""
        self.rmr_label.setText(f"RMR: {results.rmr}")
        self.q_label.setText(f"Q-System: {results.q_value}")
        self.gsi_label.setText(f"GSI: {results.gsi}")
        self.support_label.setText(
            f"Support: {results.support_recommendations['category']}"
        )
