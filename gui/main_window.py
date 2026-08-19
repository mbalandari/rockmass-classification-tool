"""
Main window for Rock Mass Classification Tool.
Defines the overall layout:
- Left: Input panel
- Right top: Results panel
- Right bottom: Plot panel
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QMenuBar
from .widgets.input_panel import InputPanel
from .widgets.result_panel import ResultPanel
from .widgets.plot_panel import PlotPanel

# BACKEND IMPORTS
from src.rockmass.models import RMRInput, QSystemInput, GSIInput, ClassificationResult
from src.rockmass.rmr import compute_rmr
from src.rockmass.qsystem import compute_q
from src.rockmass.gsi import compute_gsi
from src.rockmass.support import compute_support
from src.rockmass.plotting import (
    create_rmr_bar_chart,
    create_q_radar_chart,
    create_gsi_diagram,
)

# REPORT IMPORTS
from src.rockmass.reports.report_pdf import PDFReport
from src.rockmass.reports.report_docx import DOCXReport
from src.rockmass.reports.report_txt import TXTReport

import os

REPORT_DIR = os.path.join(os.getcwd(), "reports")
os.makedirs(REPORT_DIR, exist_ok=True)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rock Mass Classification Tool")
        self.resize(1200, 800)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Layouts
        main_layout = QHBoxLayout()
        right_layout = QVBoxLayout()

        # Widgets
        self.input_panel = InputPanel()
        self.result_panel = ResultPanel()
        self.plot_panel = PlotPanel()

        # Connect the Run button to backend logic
        self.input_panel.run_button.clicked.connect(self.run_classification)

        # Assemble right side
        right_layout.addWidget(self.result_panel, stretch=1)
        right_layout.addWidget(self.plot_panel, stretch=2)

        # Assemble main layout
        main_layout.addWidget(self.input_panel, stretch=1)
        main_layout.addLayout(right_layout, stretch=2)

        central.setLayout(main_layout)

        # Menu bar
        self._create_menu()

    def _create_menu(self):
        """Create menu bar with export options."""
        menu = QMenuBar()
        self.setMenuBar(menu)

        file_menu = menu.addMenu("File")
        export_menu = menu.addMenu("Export")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        export_pdf_action = export_menu.addAction("Export PDF")
        export_docx_action = export_menu.addAction("Export DOCX")
        export_txt_action = export_menu.addAction("Export TXT")

        export_pdf_action.triggered.connect(self.export_pdf)
        export_docx_action.triggered.connect(self.export_docx)
        export_txt_action.triggered.connect(self.export_txt)

    def run_classification(self):
        """Read inputs, run backend classification, update results and plots."""

        # RMR input
        rmr_input = RMRInput(
            ucs=float(self.input_panel.ucs.text() or 0),
            rqd=float(self.input_panel.rqd.text() or 0),
            joint_spacing=float(self.input_panel.joint_spacing.text() or 0),
            joint_condition=self.input_panel.joint_condition.text() or "rough",
            groundwater=self.input_panel.groundwater.text() or "damp",
            orientation=self.input_panel.orientation.text() or "fair",
        )

        # Q-System input
        q_input = QSystemInput(
            rqd=float(self.input_panel.rqd.text() or 0),
            jn=float(self.input_panel.jn.text() or 1),
            jr=float(self.input_panel.jr.text() or 1),
            ja=float(self.input_panel.ja.text() or 1),
            jw=float(self.input_panel.jw.text() or 1),
            srf=float(self.input_panel.srf.text() or 1),
        )

        # GSI input
        gsi_input = GSIInput(
            structure=self.input_panel.structure.text() or "blocky",
            surface_condition=self.input_panel.surface_condition.text()
            or "slightly_weathered",
            weathering=self.input_panel.weathering.text() or "moderate",
        )

        # Backend computations
        rmr_value, rmr_breakdown = compute_rmr(rmr_input)
        q_value, q_breakdown = compute_q(q_input)
        gsi_value, gsi_breakdown = compute_gsi(gsi_input)
        support = compute_support(q_value)

        # Combined result
        result = ClassificationResult(
            rmr=rmr_value,
            rmr_breakdown=rmr_breakdown,
            q_value=q_value,
            q_breakdown=q_breakdown,
            gsi=gsi_value,
            gsi_breakdown=gsi_breakdown,
            support_recommendations=support,
        )

        # Store last result for exporting
        self.last_result = result

        # Update GUI
        self.result_panel.update_results(result)

        # Update plot (RMR chart for now)
        fig = create_rmr_bar_chart(rmr_breakdown)
        self.plot_panel.update_plot(fig)

    def export_pdf(self):
        """Export PDF report."""
        if not hasattr(self, "last_result"):
            return
        report = PDFReport(self.last_result)
        report.generate(os.path.join(REPORT_DIR, "rockmass_report.pdf"))

    def export_docx(self):
        """Export DOCX report."""
        if not hasattr(self, "last_result"):
            return
        report = DOCXReport(self.last_result)
        report.generate(os.path.join(REPORT_DIR, "rockmass_report.docx"))

    def export_txt(self):
        """Export TXT report."""
        if not hasattr(self, "last_result"):
            return
        report = TXTReport(self.last_result)
        report.generate(os.path.join(REPORT_DIR, "rockmass_report.txt"))
