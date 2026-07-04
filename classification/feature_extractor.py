"""
Feature Extractor

Extracts low-level image features that help verify
AI predictions.

Features:
- Width
- Height
- Aspect Ratio
- Brightness
- Contrast
- Variance
- Saturation
- Edge Density
- Entropy
- Sharpness
"""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image


class FeatureExtractor:

    def __init__(self):
        pass

    def _load_image(self, image):

        if isinstance(image, (str, Path)):
            image = Image.open(image).convert("RGB")

        return image

    def extract(self, image):

        image = self._load_image(image)

        rgb = np.array(image)

        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

        height, width = gray.shape

        # ----------------------------
        # Basic Information
        # ----------------------------

        aspect_ratio = width / height

        megapixels = (width * height) / 1_000_000

        # ----------------------------
        # Brightness
        # ----------------------------

        brightness = float(np.mean(gray) / 255.0)

        # ----------------------------
        # Contrast
        # ----------------------------

        contrast = float(np.std(gray) / 255.0)

        # ----------------------------
        # Variance
        # ----------------------------

        variance = float(np.var(gray) / (255.0 ** 2))

        # ----------------------------
        # Saturation
        # ----------------------------

        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)

        saturation = float(np.mean(hsv[:, :, 1]) / 255.0)

        # ----------------------------
        # Edge Density
        # ----------------------------

        edges = cv2.Canny(gray, 100, 200)

        edge_density = float(np.count_nonzero(edges) / edges.size)

        # ----------------------------
        # Sharpness
        # ----------------------------

        sharpness = float(
            cv2.Laplacian(gray, cv2.CV_64F).var()
        )

        # ----------------------------
        # Entropy
        # ----------------------------

        histogram = cv2.calcHist(
            [gray],
            [0],
            None,
            [256],
            [0, 256],
        )

        histogram = histogram.ravel()

        histogram = histogram / histogram.sum()

        entropy = float(
            -np.sum(
                histogram * np.log2(histogram + 1e-8)
            )
        )

        # ----------------------------
        # Color Statistics
        # ----------------------------

        rgb_mean = np.mean(rgb, axis=(0, 1))

        rgb_std = np.std(rgb, axis=(0, 1))

        return {

            "width": width,

            "height": height,

            "megapixels": round(megapixels, 2),

            "aspect_ratio": round(aspect_ratio, 3),

            "brightness": round(brightness, 4),

            "contrast": round(contrast, 4),

            "variance": round(variance, 4),

            "saturation": round(saturation, 4),

            "edge_density": round(edge_density, 4),

            "entropy": round(entropy, 4),

            "sharpness": round(sharpness, 2),

            "rgb_mean": rgb_mean.tolist(),

            "rgb_std": rgb_std.tolist()

        }


feature_extractor = FeatureExtractor()