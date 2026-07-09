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

        # Same defaults as logger.py, for the same reason: existing
        # call sites (corrupted/duplicate/unknown) don't have these.
        orientation="-",

        scene_type="-",

        has_ui_elements="-",

        wallpaper_suitable="-",

        description="-",

        wallpaper_reason="-",

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

            "status": status,

            "orientation": orientation,

            "scene_type": scene_type,

            "has_ui_elements": has_ui_elements,

            "wallpaper_suitable": wallpaper_suitable,

            "description": description,

            "wallpaper_reason": wallpaper_reason,

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