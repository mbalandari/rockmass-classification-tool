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

        # Later we will connect these actions
        file_menu.addAction("Exit")
        export_menu.addAction("Export PDF")
        export_menu.addAction("Export DOCX")
        export_menu.addAction("Export TXT")
