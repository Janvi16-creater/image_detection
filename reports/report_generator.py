"""
Report Generator

Collects processed image information and
generates reports.
"""

from reports.statistics import statistics
from reports.exporter import exporter


class ReportGenerator:

    def __init__(self):

        self.records = []

    # ------------------------------------------

    def add_record(

        self,

        filename,

        category,

        confidence,
        
        source,

        blur,

        noise,

        exposure,

        resolution,

        status,

    ):

        record = {

            "filename": filename,

            "category": category,

            "confidence": confidence,
            
            "source": source,

            "blur": blur,

            "noise": noise,

            "exposure": exposure,

            "resolution": resolution,

            "status": status

        }

        self.records.append(record)

        statistics.add_record(record)

    # ------------------------------------------

    def save(self):

        print(f"\nSaving reports for {len(self.records)} records...")
        print(f"Records contents: {self.records}")

        summary = statistics.generate()

        exporter.export_csv(
            self.records
        )

        exporter.export_json(
            self.records
        )

        exporter.export_summary(
            summary
        )

        print("\nReport Generated Successfully")

        print(
            "Saved to output/reports/"
        )


report_generator = ReportGenerator()