"""
Main window for Rock Mass Classification Tool.
Defines the overall layout:
- Left: Input panel
- Right top: Results panel
- Right bottom: Plot panel
"""

import os

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QMenuBar,
    QMessageBox,
)
from PySide6.QtGui import QAction

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

REPORT_DIR = os.path.join(os.getcwd(), "reports")
os.makedirs(REPORT_DIR, exist_ok=True)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rock Mass Classification Tool")
        self.resize(1200, 800)

        # Central widget and main layout
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()
        right_layout = QVBoxLayout()

        # Panels
        self.input_panel = InputPanel()
        self.result_panel = ResultPanel()
        self.plot_panel = PlotPanel()

        # Connect the Run button to backend logic
        self.input_panel.run_button.clicked.connect(self.run_classification)

        # Assemble right side (top: results, bottom: plot)
        right_layout.addWidget(self.result_panel, stretch=1)
        right_layout.addWidget(self.plot_panel, stretch=2)

        # Assemble main layout (left: input, right: results+plot)
        main_layout.addWidget(self.input_panel, stretch=1)
        main_layout.addLayout(right_layout, stretch=2)

        central.setLayout(main_layout)

        # Menu bar
        self._create_menu()

        # Last result placeholder
        self.last_result: ClassificationResult | None = None

    def _create_menu(self):
        """Create menu bar with export options and About."""
        menubar: QMenuBar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Export menu
        export_menu = menubar.addMenu("Export")

        export_pdf_action = QAction("Export PDF", self)
        export_pdf_action.triggered.connect(self.export_pdf)
        export_menu.addAction(export_pdf_action)

        export_docx_action = QAction("Export DOCX", self)
        export_docx_action.triggered.connect(self.export_docx)
        export_menu.addAction(export_docx_action)

        export_txt_action = QAction("Export TXT", self)
        export_txt_action.triggered.connect(self.export_txt)
        export_menu.addAction(export_txt_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

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

        # Update GUI results
        self.result_panel.update_results(result)

        # Update plot (RMR chart for now; Q and GSI are in reports)
        fig = create_rmr_bar_chart(rmr_breakdown)
        self.plot_panel.update_plot(fig)

        QMessageBox.information(
            self,
            "Classification Complete",
            "Rock mass classification has been computed successfully.",
        )

    def _ensure_result(self) -> bool:
        if self.last_result is None:
            QMessageBox.warning(
                self,
                "No Result",
                "Please run the classification before exporting a report.",
            )
            return False
        return True

    def export_pdf(self):
        """Export PDF report."""
        if not self._ensure_result():
            return
        report = PDFReport(self.last_result)
        path = os.path.join(REPORT_DIR, "rockmass_report.pdf")
        report.generate(path)
        QMessageBox.information(
            self,
            "Export Successful",
            f"PDF report saved to:\n{path}",
        )

    def export_docx(self):
        """Export DOCX report."""
        if not self._ensure_result():
            return
        report = DOCXReport(self.last_result)
        path = os.path.join(REPORT_DIR, "rockmass_report.docx")
        report.generate(path)
        QMessageBox.information(
            self,
            "Export Successful",
            f"DOCX report saved to:\n{path}",
        )

    def export_txt(self):
        """Export TXT report."""
        if not self._ensure_result():
            return
        report = TXTReport(self.last_result)
        path = os.path.join(REPORT_DIR, "rockmass_report.txt")
        report.generate(path)
        QMessageBox.information(
            self,
            "Export Successful",
            f"TXT report saved to:\n{path}",
        )

    def show_about_dialog(self):
        QMessageBox.information(
            self,
            "About RockMass Classifier",
            (
                "RockMass Classifier\n"
                "Version 1.0\n\n"
                "A professional rock mass classification tool based on:\n"
                "- RMR (Bieniawski)\n"
                "- Q-System (Barton et al.)\n"
                "- GSI (Hoek & Marinos)\n\n"
                "Features:\n"
                "- Engineering-grade charts\n"
                "- PDF, DOCX, TXT reporting\n"
                "- Clean GUI for fast input\n\n"
                "Developed by Maz."
            ),
        )
