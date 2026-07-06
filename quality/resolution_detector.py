"""
Resolution Detector

Checks image resolution and categorizes it.

Returns
-------
{
    "width": int,
    "height": int,
    "megapixels": float,
    "aspect_ratio": float,
    "orientation": str,
    "resolution_label": str,
    "is_good_resolution": bool
}
"""

from pathlib import Path

import numpy as np
from PIL import Image


class ResolutionDetector:

    def __init__(self):

        self.minimum_width = 720
        self.minimum_height = 720

    # ---------------------------------------------------------

    def _load_image(self, image):

        if isinstance(image, (str, Path)):

            image = Image.open(image).convert("RGB")

        return np.array(image)

    # ---------------------------------------------------------

    def detect(self, image):

        image = self._load_image(image)

        height, width = image.shape[:2]

        megapixels = (width * height) / 1_000_000

        aspect_ratio = width / height

        # --------------------------------------------
        # Orientation
        # --------------------------------------------

        if width > height:

            orientation = "landscape"

        elif width < height:

            orientation = "portrait"

        else:

            orientation = "square"

        # --------------------------------------------
        # Resolution Label
        # --------------------------------------------

        if width >= 7680 and height >= 4320:

            label = "8K"

        elif width >= 3840 and height >= 2160:

            label = "4K"

        elif width >= 2560 and height >= 1440:

            label = "2K"

        elif width >= 1920 and height >= 1080:

            label = "Full HD"

        elif width >= 1280 and height >= 720:

            label = "HD"

        else:

            label = "Low Resolution"

        # --------------------------------------------
        # Quality Check
        # --------------------------------------------

        is_good = (
            width >= self.minimum_width
            and
            height >= self.minimum_height
        )

        return {

            "width": width,

            "height": height,

            "megapixels": round(
                megapixels,
                2
            ),

            "aspect_ratio": round(
                aspect_ratio,
                3
            ),

            "orientation": orientation,

            "resolution_label": label,

            "is_good_resolution": is_good

        }


resolution_detector = ResolutionDetector()