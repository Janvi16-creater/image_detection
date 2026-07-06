"""
Statistics Module

Calculates statistics for the processed dataset.
"""

from collections import Counter


class Statistics:

    def __init__(self):
        self.records = []

    def add_record(self, record):
        """
        Add a processed image record.
        """
        self.records.append(record)

    def generate(self):

        print(f"Statistics records count: {len(self.records)}")
        total = len(self.records)

        categories = Counter()

        accepted = 0
        rejected = 0

        blurry = 0
        noisy = 0
        overexposed = 0
        underexposed = 0
        low_resolution = 0

        confidence_sum = 0

        for record in self.records:

            category = record.get("category", "unknown")
            categories[category] += 1

            confidence_sum += record.get("confidence", 0)

            if record.get("status") == "Accepted":
                accepted += 1
            else:
                rejected += 1

            if record.get("blur") in ("blurry", "extremely_blurry"):
                blurry += 1

            if record.get("noise") in (
                "moderate_noise",
                "high_noise",
            ):
                noisy += 1

            exposure = record.get("exposure")

            if exposure == "overexposed":
                overexposed += 1

            if exposure == "underexposed":
                underexposed += 1

            if record.get("resolution") == "Low Resolution":
                low_resolution += 1

        avg_confidence = 0

        if total != 0:
            avg_confidence = confidence_sum / total

        return {

            "total_images": total,

            "accepted": accepted,

            "rejected": rejected,

            "categories": dict(categories),

            "blurry": blurry,

            "noisy": noisy,

            "overexposed": overexposed,

            "underexposed": underexposed,

            "low_resolution": low_resolution,

            "average_confidence": round(
                avg_confidence,
                3,
            )

        }


statistics = Statistics()