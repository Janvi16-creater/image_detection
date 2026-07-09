"""
Blur Detector

Detects image sharpness using the Variance of Laplacian.

Reference:
    OpenCV - Variance of Laplacian

Returns:
    {
        "laplacian_variance": float,
        "blur_score": float,
        "label": str,
        "is_blurry": bool
    }
"""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image


class BlurDetector:
    """
    Detect image blur using Variance of Laplacian.

    Interpretation:

        < 50      Extremely Blurry

        50-120    Blurry

        120-250   Moderate

        >250      Sharp

    These values work well for most datasets and can
    be adjusted depending on image resolution.
    """

    def __init__(self):

        self.extremely_blurry = 50

        self.blurry = 120

        self.sharp = 250

    # --------------------------------------------------

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

    # --------------------------------------------------

    def detect(self, image):

        gray = self._load_image(image)

        laplacian_variance = cv2.Laplacian(
            gray,
            cv2.CV_64F
        ).var()

        blur_score = float(laplacian_variance)

        if blur_score < self.extremely_blurry:

            label = "extremely_blurry"

            is_blurry = True

        elif blur_score < self.blurry:

            label = "blurry"

            is_blurry = True

        elif blur_score < self.sharp:

            label = "moderately_sharp"

            is_blurry = False

        else:

            label = "sharp"

            is_blurry = False

        return {

            "laplacian_variance": round(
                blur_score,
                2
            ),

            "blur_score": round(
                blur_score,
                2
            ),

            "label": label,

            "is_blurry": is_blurry

        }

    # --------------------------------------------------

    # UNUSED
    # def batch_detect(self, image_paths):
    #     results = []
    #     for image in image_paths:
    #         result = self.detect(image)
    #         result["image"] = str(image)
    #         results.append(result)
    #     return results


blur_detector = BlurDetector()