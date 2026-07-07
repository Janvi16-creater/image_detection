"""
Exposure Detector

Detects whether an image is

- Underexposed
- Properly Exposed
- Overexposed

Returns
-------
{
    "mean_brightness": float,
    "dark_ratio": float,
    "bright_ratio": float,
    "label": str,
    "is_good_exposure": bool
}
"""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image


class ExposureDetector:

    def __init__(self):

        self.dark_threshold = 50

        self.bright_threshold = 205

    # ------------------------------------------------

    def _load_image(self, image):

        if isinstance(image, (str, Path)):

            image = Image.open(image).convert("RGB")
            image = np.array(image)
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        else:

            # Already a numpy array from cv2.imread (BGR)
            image = np.array(image)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        return gray

    # ------------------------------------------------

    def detect(self, image):

        gray = self._load_image(image)

        brightness = float(np.mean(gray))

        dark_pixels = np.sum(
            gray < self.dark_threshold
        )

        bright_pixels = np.sum(
            gray > self.bright_threshold
        )

        total_pixels = gray.size

        dark_ratio = dark_pixels / total_pixels

        bright_ratio = bright_pixels / total_pixels

        if brightness < 70:

            label = "underexposed"

            good = False

        elif brightness > 185:

            label = "overexposed"

            good = False

        else:

            label = "properly_exposed"

            good = True

        return {

            "mean_brightness": round(
                brightness,
                2
            ),

            "dark_ratio": round(
                dark_ratio,
                4
            ),

            "bright_ratio": round(
                bright_ratio,
                4
            ),

            "label": label,

            "is_good_exposure": good

        }


exposure_detector = ExposureDetector()