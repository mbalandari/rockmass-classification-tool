"""
Panel for displaying charts using Matplotlib.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure


class PlotPanel(QWidget):
    """Displays RMR, Q-System, and GSI charts."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.fig = Figure(figsize=(5, 4))
        self.canvas = Canvas(self.fig)

        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_plot(self, fig):
        """Replace current figure with new one."""
        self.fig.clear()

        # Copy axes from provided figure
        src_ax = fig.axes[0]
        dst_ax = self.fig.add_subplot(111)

        for line in src_ax.lines:
            dst_ax.plot(line.get_xdata(), line.get_ydata())

        dst_ax.set_title(src_ax.get_title())
        dst_ax.set_xlabel(src_ax.get_xlabel())
        dst_ax.set_ylabel(src_ax.get_ylabel())

        self.fig.tight_layout()
        self.canvas.draw()
