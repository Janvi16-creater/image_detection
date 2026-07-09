"""
Logger

Creates a processing log.

Every processed image is written to a CSV.
"""

import csv
import time

from pathlib import Path


class ProcessingLogger:

    FIELDNAMES = [

        "filename",

        "category",

        "confidence",

        "source",

        "blur",

        "noise",

        "exposure",

        "resolution",

        "status",

        "orientation",

        "scene_type",

        "has_ui_elements",

        "wallpaper_suitable",

        "description",

        "wallpaper_reason",

    ]

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

                writer.writerow(self.FIELDNAMES)

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

        status,

        # New fields default to "-" so every existing call site
        # (corrupted/duplicate/unknown branches, which don't have
        # Gemini's extra detail) keeps working without changes.
        orientation="-",

        scene_type="-",

        has_ui_elements="-",

        wallpaper_suitable="-",

        description="-",

        wallpaper_reason="-",

    ):

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
                        source,
                        blur,
                        noise,
                        exposure,
                        resolution,
                        status,
                        orientation,
                        scene_type,
                        has_ui_elements,
                        wallpaper_suitable,
                        description,
                        wallpaper_reason,
                    ])
                return
            except PermissionError:
                if attempt == 4:
                    raise
                time.sleep(0.1)


logger = ProcessingLogger()