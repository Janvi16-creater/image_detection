"""
Exporter

Exports reports into

- CSV
- JSON
- TXT Summary
"""

import csv
import json
from pathlib import Path


class Exporter:

    def __init__(self):

        self.output_dir = Path("output/reports")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # --------------------------------------

    def export_csv(self, records):

        csv_file = self.output_dir / "dataset_report.csv"

        if len(records) == 0:
            return

        keys = records[0].keys()

        with open(
            csv_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=keys,
            )

            writer.writeheader()

            writer.writerows(records)

    # --------------------------------------

    def export_json(self, records):

        json_file = self.output_dir / "dataset_report.json"

        with open(
            json_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                records,
                file,
                indent=4
            )

    # --------------------------------------

    def export_summary(self, summary):

        txt_file = self.output_dir / "summary.txt"

        with open(
            txt_file,
            "w",
            encoding="utf-8"
        ) as file:

            for key, value in summary.items():

                file.write(
                    f"{key}: {value}\n"
                )


exporter = Exporter()