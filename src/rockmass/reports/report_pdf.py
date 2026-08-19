import os

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

from src.rockmass.plotting import (
    create_rmr_bar_chart,
    create_q_radar_chart,
    create_gsi_diagram,
    save_figure_as_png,
)


class PDFReport:
    def __init__(self, result):
        # ClassificationResult object
        self.result = result
        self.styles = getSampleStyleSheet()

    # ---------------------------------------------------------
    # TABLE CREATION (ReportLab version)
    # ---------------------------------------------------------
    def _create_table(self, title, data_dict):
        """
        Returns a ReportLab Table flowable.
        """
        style_title = self.styles["Heading3"]
        title_paragraph = Paragraph(title, style_title)

        # Convert dict to table rows
        rows = [["Parameter", "Value"]]
        for key, value in data_dict.items():
            rows.append([str(key), str(value)])

        table = Table(rows, colWidths=[200, 200])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ]
            )
        )

        return [title_paragraph, Spacer(1, 6), table, Spacer(1, 12)]

    # ---------------------------------------------------------
    # MAIN REPORT GENERATION
    # ---------------------------------------------------------
    def generate(self, output_path: str):
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        doc = SimpleDocTemplate(output_path, pagesize=A4)
        elements = []

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------
        elements.append(
            Paragraph("Rock Mass Classification Report", self.styles["Title"])
        )
        elements.append(Spacer(1, 12))

        # -----------------------------------------------------
        # SUMMARY
        # -----------------------------------------------------
        summary = (
            f"<b>RMR:</b> {self.result.rmr:.2f}<br/>"
            f"<b>Q-System:</b> {self.result.q_value:.2f}<br/>"
            f"<b>GSI:</b> {self.result.gsi:.2f}<br/><br/>"
            f"<b>Support Recommendations:</b><br/>{self.result.support_recommendations}"
        )
        elements.append(Paragraph(summary, self.styles["BodyText"]))
        elements.append(Spacer(1, 12))

        # -----------------------------------------------------
        # TABLES
        # -----------------------------------------------------
        elements.extend(self._create_table("RMR Breakdown", self.result.rmr_breakdown))
        elements.extend(
            self._create_table("Q-System Breakdown", self.result.q_breakdown)
        )
        elements.extend(self._create_table("GSI Breakdown", self.result.gsi_breakdown))

        # -----------------------------------------------------
        # GENERATE CHARTS
        # -----------------------------------------------------
        rmr_fig = create_rmr_bar_chart(self.result.rmr_breakdown)
        q_fig = create_q_radar_chart(self.result.q_breakdown)
        gsi_fig = create_gsi_diagram(
            self.result.gsi_breakdown, gsi_value=self.result.gsi
        )

        rmr_path = os.path.join(output_dir, "rmr_chart.png")
        q_path = os.path.join(output_dir, "q_chart.png")
        gsi_path = os.path.join(output_dir, "gsi_chart.png")

        save_figure_as_png(rmr_fig, rmr_path)
        save_figure_as_png(q_fig, q_path)
        save_figure_as_png(gsi_fig, gsi_path)

        # -----------------------------------------------------
        # INSERT CHARTS
        # -----------------------------------------------------
        elements.append(Paragraph("RMR Breakdown Chart", self.styles["Heading3"]))
        elements.append(Image(rmr_path, width=400, height=300))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Q-System Chart", self.styles["Heading3"]))
        elements.append(Image(q_path, width=400, height=300))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("GSI Diagram", self.styles["Heading3"]))
        elements.append(Image(gsi_path, width=400, height=300))
        elements.append(Spacer(1, 12))

        # -----------------------------------------------------
        # BUILD PDF
        # -----------------------------------------------------
        doc.build(elements)
