"""
OCR Detector

Runs OCR ONLY when
ScreenshotDetector says the image
is a screenshot candidate.
"""

import easyocr


class OCRDetector:

    def __init__(self):

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False,
            download_enabled=True,
        )

    # ----------------------------------------------------------

    def detect(self, image_path):

        results = self.reader.readtext(
            str(image_path),
            detail=0,
        )

        words = []

        for text in results:

            text = text.strip()

            if text:

                words.append(text)

        return {

            "word_count": len(words),

            "text": words

        }


ocr_detector = OCRDetector()