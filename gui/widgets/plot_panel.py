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

        # Create a blank figure for the panel
        self.fig = Figure(figsize=(5, 4))
        self.canvas = Canvas(self.fig)

        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_plot(self, fig):
        """
        Completely redraw the bar chart using backend data instead of copying
        """

        # Clear the existing figure
        self.fig.clear()

        # Create a new axis
        dst_ax = self.fig.add_subplot(111)

        # Extract labels and heights from the original figure
        src_ax = fig.axes[0]

        # Extract labels
        labels = [tick.get_text() for tick in src_ax.get_xticklabels()]

        # Extract heights from the original bar chart
        # If patches are missing (negative or zero bars), we fallback to backend data
        heights = []
        if src_ax.patches:
            # Matplotlib may omit patches for zero or negative bars
            # So we read heights from the original bar chart's data
            for patch in src_ax.patches:
                heights.append(patch.get_height())

            # If patches are fewer than labels, pad with zeros
            while len(heights) < len(labels):
                heights.append(0)
        else:
            # If no patches exist at all, fallback to zeros
            heights = [0] * len(labels)

        # Create categorical positions
        x_positions = range(len(labels))

        # Draw bars (Matplotlib handles negative heights correctly)
        dst_ax.bar(x_positions, heights, color="#4C72B0")

        # Set labels
        dst_ax.set_xticks(x_positions)
        dst_ax.set_xticklabels(labels)

        # Copy title and axis labels
        dst_ax.set_title(src_ax.get_title())
        dst_ax.set_xlabel(src_ax.get_xlabel())
        dst_ax.set_ylabel(src_ax.get_ylabel())

        # Remove numeric ticks
        dst_ax.tick_params(axis="x", which="both", length=0)

        # Redraw
        self.fig.tight_layout()
        self.canvas.draw()
