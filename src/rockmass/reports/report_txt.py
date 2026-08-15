"""
report_txt.py
-------------
Simple text report for fallback or debugging.
"""


class TXTReport:
    def __init__(self, results):
        self.results = results

    def generate(self, path: str):
        with open(path, "w") as f:
            f.write("Rock Mass Classification Report\n")
            f.write("===============================\n\n")

            f.write("RMR Breakdown:\n")
            for k, v in self.results.rmr_breakdown.items():
                f.write(f"  {k}: {v}\n")

            f.write("\nQ-System Breakdown:\n")
            for k, v in self.results.q_breakdown.items():
                f.write(f"  {k}: {v}\n")

            f.write("\nGSI Breakdown:\n")
            for k, v in self.results.gsi_breakdown.items():
                f.write(f"  {k}: {v}\n")

            f.write("\nSupport Recommendations:\n")
            for k, v in self.results.support_recommendations.items():
                f.write(f"  {k}: {v}\n")
