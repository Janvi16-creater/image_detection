"""
Feature Extractor

Extracts lightweight visual features using OpenCV.

This module is intentionally fast because it runs on every image.

Returned features are later used by:
    - Wallpaper Detector
    - Camera Detector
    - Screenshot Detector
    - Widget Detector
    - Decision Engine
"""

from pathlib import Path

import cv2
import numpy as np


class FeatureExtractor:

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def extract(self, image):

        if image is None:

            raise ValueError("Unable to read image: image is None")

        height, width = image.shape[:2]

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # -----------------------------------------------------
        # Basic Image Information
        # -----------------------------------------------------

        aspect_ratio = width / height

        megapixels = (width * height) / 1_000_000

        # -----------------------------------------------------
        # Brightness
        # -----------------------------------------------------

        brightness = float(np.mean(gray))

        # -----------------------------------------------------
        # Contrast
        # -----------------------------------------------------

        contrast = float(np.std(gray))

        # -----------------------------------------------------
        # Sharpness
        # -----------------------------------------------------

        sharpness = float(
            cv2.Laplacian(gray, cv2.CV_64F).var()
        )

        # -----------------------------------------------------
        # Edge Density
        # -----------------------------------------------------

        edges = cv2.Canny(
            gray,
            100,
            200
        )

        edge_density = float(
            np.count_nonzero(edges)
            /
            edges.size
        )

        # -----------------------------------------------------
        # Entropy
        # -----------------------------------------------------

        histogram = cv2.calcHist(
            [gray],
            [0],
            None,
            [256],
            [0, 256]
        )

        histogram = histogram.ravel()

        histogram /= histogram.sum()

        entropy = float(

            -np.sum(

                histogram * np.log2(
                    histogram + 1e-8
                )

            )

        )

        # -----------------------------------------------------
        # Color Statistics
        # -----------------------------------------------------

        hsv = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2HSV
        )

        saturation = float(
            np.mean(hsv[:, :, 1])
        )

        value = float(
            np.mean(hsv[:, :, 2])
        )

        color_variance = float(
            np.var(
                image.reshape(-1, 3),
                axis=0
            ).mean()
        )

        # -----------------------------------------------------
        # Center Region Analysis
        # -----------------------------------------------------

        h1 = height // 4
        h2 = 3 * height // 4

        w1 = width // 4
        w2 = 3 * width // 4

        center = gray[h1:h2, w1:w2]

        center_edges = cv2.Canny(
            center,
            100,
            200
        )

        center_edge_density = float(

            np.count_nonzero(center_edges)

            /

            center_edges.size

        )

        center_brightness = float(
            np.mean(center)
        )

        center_contrast = float(
            np.std(center)
        )

        # -----------------------------------------------------
        # Horizontal / Vertical Line Density
        # -----------------------------------------------------

        lines = cv2.HoughLinesP(

            edges,

            1,

            np.pi / 180,

            threshold=100,

            minLineLength=80,

            maxLineGap=10

        )

        horizontal_lines = 0
        vertical_lines = 0

        if lines is not None:

            for line in lines:

                # Handle different OpenCV output formats
                if len(line.shape) == 2:
                    x1, y1, x2, y2 = line[0]
                else:
                    x1, y1, x2, y2 = line

                # Horizontal line
                if abs(y2 - y1) <= 5:
                    horizontal_lines += 1

                # Vertical line
                if abs(x2 - x1) <= 5:
                    vertical_lines += 1

        # -----------------------------------------------------
        # Return All Features
        # -----------------------------------------------------

        return {

            "width": width,

            "height": height,

            "megapixels": megapixels,

            "aspect_ratio": aspect_ratio,

            "brightness": brightness,

            "contrast": contrast,

            "sharpness": sharpness,

            "edge_density": edge_density,

            "entropy": entropy,

            "saturation": saturation,

            "value": value,

            "color_variance": color_variance,

            "center_edge_density": center_edge_density,

            "center_brightness": center_brightness,

            "center_contrast": center_contrast,

            "horizontal_lines": horizontal_lines,

            "vertical_lines": vertical_lines

        }


feature_extractor = FeatureExtractor()