"""
Noise Detector

Detects image noise using local variance analysis.

Returns:
{
    "noise_score": float,
    "label": str,
    "is_noisy": bool
}
"""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image


class NoiseDetector:
    """
    Detect image noise.

    Categories:

        < 5      Very Clean

        5-15     Low Noise

        15-30    Moderate Noise

        >30      High Noise
    """

    def __init__(self):

        self.low_noise = 5

        self.medium_noise = 15

        self.high_noise = 30

    # --------------------------------------------------

    def _load_image(self, image):

        if isinstance(image, (str, Path)):

            image = Image.open(image).convert("RGB")

        image = np.array(image)

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_RGB2GRAY
        )

        return gray

    # --------------------------------------------------

    def detect(self, image):

        gray = self._load_image(image)

        # Median filter removes most noise while
        # preserving edges.
        median = cv2.medianBlur(gray, 3)

        # Difference between original and filtered image
        difference = cv2.absdiff(gray, median)

        noise_score = float(np.std(difference))

        if noise_score < self.low_noise:

            label = "very_clean"

            is_noisy = False

        elif noise_score < self.medium_noise:

            label = "low_noise"

            is_noisy = False

        elif noise_score < self.high_noise:

            label = "moderate_noise"

            is_noisy = True

        else:

            label = "high_noise"

            is_noisy = True

        return {

            "noise_score": round(
                noise_score,
                2
            ),

            "label": label,

            "is_noisy": is_noisy

        }

    # --------------------------------------------------

    def batch_detect(self, image_paths):

        results = []

        for image in image_paths:

            result = self.detect(image)

            result["image"] = str(image)

            results.append(result)

        return results


noise_detector = NoiseDetector()