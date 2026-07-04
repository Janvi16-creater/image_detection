"""
OCR Detector

Uses EasyOCR to detect text in an image.

Returned information:
- text_count
- total_characters
- average_confidence
- text_density
- detected_text
"""

from pathlib import Path

import easyocr
import numpy as np
from PIL import Image


class OCRDetector:
    """
    Singleton OCR detector.
    """

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance._initialize()

        return cls._instance

    def _initialize(self):

        # GPU automatically used if available
        self.reader = easyocr.Reader(
            ['en'],
            gpu=True
        )

    def _load_image(self, image):

        if isinstance(image, (str, Path)):
            image = Image.open(image).convert("RGB")

        return np.array(image)

    def detect(self, image):

        image = self._load_image(image)

        height, width = image.shape[:2]

        image_area = width * height

        results = self.reader.readtext(image)

        detected_text = []

        total_area = 0

        confidence_sum = 0

        for box, text, confidence in results:

            detected_text.append(text)

            confidence_sum += confidence

            x = [p[0] for p in box]
            y = [p[1] for p in box]

            area = (
                (max(x) - min(x))
                *
                (max(y) - min(y))
            )

            total_area += area

        text_count = len(results)

        total_characters = sum(
            len(text)
            for text in detected_text
        )

        average_confidence = (

            confidence_sum / text_count

            if text_count

            else 0

        )

        text_density = (

            total_area / image_area

            if image_area

            else 0

        )

        return {

            "text_count": text_count,

            "total_characters": total_characters,

            "average_confidence": round(
                average_confidence,
                4
            ),

            "text_density": round(
                text_density,
                4
            ),

            "detected_text": detected_text

        }


ocr_detector = OCRDetector()