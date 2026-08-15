"""
report_docx.py
--------------
Generates a professional DOCX report using python-docx.
"""

from docx import Document


class DOCXReport:
    """Creates a DOCX geotechnical report."""

    def __init__(self, results):
        self.results = results

    def generate(self, path: str):
        doc = Document()

        doc.add_heading("Rock Mass Classification Report", level=1)

        doc.add_heading("RMR Breakdown", level=2)
        self._add_table(doc, self.results.rmr_breakdown)

        doc.add_heading("Q-System Breakdown", level=2)
        self._add_table(doc, self.results.q_breakdown)

        doc.add_heading("GSI Breakdown", level=2)
        self._add_table(doc, self.results.gsi_breakdown)

        doc.add_heading("Support Recommendations", level=2)
        self._add_table(doc, self.results.support_recommendations)

        doc.save(path)

    def _add_table(self, doc, data: dict):
        table = doc.add_table(rows=1, cols=2)
        hdr = table.rows[0].cells
        hdr[0].text = "Parameter"
        hdr[1].text = "Value"

        for key, value in data.items():
            row = table.add_row().cells
            row[0].text = key
            row[1].text = str(value)
