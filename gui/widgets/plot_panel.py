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
        Redraw the provided Matplotlib figure inside this panel.
        """

        # Clear the existing figure
        self.fig.clear()

        # Create a new axis
        dst_ax = self.fig.add_subplot(111)

        # Get the source axis
        src_ax = fig.axes[0]

        # --- HANDLE BAR CHARTS ---
        if src_ax.patches:
            # Extract labels from original chart
            original_labels = [tick.get_text() for tick in src_ax.get_xticklabels()]

            # Extract bar heights and colors
            heights = []
            colors = []

            for patch in src_ax.patches:
                heights.append(patch.get_height())
                colors.append(patch.get_facecolor())

            # Create new categorical positions
            x_positions = range(len(heights))

            # Draw bars
            dst_ax.bar(x_positions, heights, color=colors)

            # Set correct labels
            dst_ax.set_xticks(x_positions)
            dst_ax.set_xticklabels(original_labels)

        # --- HANDLE LINE PLOTS (Radar charts) ---
        elif src_ax.lines:
            for line in src_ax.lines:
                dst_ax.plot(
                    line.get_xdata(),
                    line.get_ydata(),
                    color=line.get_color(),
                    linestyle=line.get_linestyle(),
                    linewidth=line.get_linewidth(),
                )

        # --- COPY TITLES & LABELS ---
        dst_ax.set_title(src_ax.get_title())
        dst_ax.set_xlabel(src_ax.get_xlabel())
        dst_ax.set_ylabel(src_ax.get_ylabel())

        # --- COPY LIMITS ---
        dst_ax.set_ylim(src_ax.get_ylim())

        # Remove numeric ticks entirely
        dst_ax.tick_params(axis="x", which="both", length=0)

        # Redraw
        self.fig.tight_layout()
        self.canvas.draw()
