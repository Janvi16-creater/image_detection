"""
Logger

Creates a processing log.

Every processed image is written to a CSV.
"""

import csv
from pathlib import Path


class ProcessingLogger:

    def __init__(

        self,

        log_file="output/processing_log.csv"

    ):

        self.log_file = Path(log_file)

        self.log_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.log_file.exists():

            with open(

                self.log_file,

                "w",

                newline="",

                encoding="utf-8"

            ) as file:

                writer = csv.writer(file)

                writer.writerow([

                    "filename",

                    "category",

                    "confidence",

                    "blur",

                    "noise",

                    "exposure",

                    "resolution",

                    "status"

                ])

    # --------------------------------------------------

    def log(

        self,

        filename,

        category,

        confidence,
        
        source,

        blur,

        noise,

        exposure,

        resolution,

        status

    ):

        import time
        for attempt in range(5):
            try:
                with open(
                    self.log_file,
                    "a",
                    newline="",
                    encoding="utf-8"
                ) as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        filename,
                        category,
                        confidence,
                        blur,
                        noise,
                        exposure,
                        resolution,
                        status
                    ])
                return
            except PermissionError:
                if attempt == 4:
                    raise
                time.sleep(0.1)


logger = ProcessingLogger()