"""Report generation helpers."""
import csv
from pathlib import Path

import pandas as pd

DEFAULT_REPORT_FIELDS = [
    "filename",
    "status",
    "category",
    "confidence",
    "reason",
    "blur_score",
    "blur_label",
    "width",
    "height",
    "resolution_label",
    "duplicate_of",
]


def start_report(output_path, fieldnames=None):
    """Create a CSV report file and return the handle and writer."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    handle = output_path.open("w", newline="", encoding="utf-8")
    writer = csv.DictWriter(handle, fieldnames=fieldnames or DEFAULT_REPORT_FIELDS)
    writer.writeheader()
    return handle, writer


def append_report_row(handle, writer, row):
    """Append a normalized row to the report writer."""
    normalized = {key: "" if value is None else value for key, value in row.items()}
    writer.writerow(normalized)


def save_report(report_rows, output_path):
    """Save report rows to CSV."""
    handle, writer = start_report(output_path)
    try:
        for row in report_rows:
            append_report_row(handle, writer, row)
    finally:
        handle.close()
    return output_path
