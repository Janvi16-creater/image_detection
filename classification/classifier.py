"""
Image Classifier

This is the public API for the classification module.

Pipeline:
Image
    │
    ▼
AI Classifier
    │
    ▼
Feature Extractor
    │
    ▼
OCR Detector
    │
    ▼
Decision Engine
    │
    ▼
Final Classification
"""

from classification.ai.ai_classifier import classifier as ai_classifier
from classification.feature_extractor import feature_extractor
from classification.ocr_detector import ocr_detector
from classification.decision_engine import decision_engine


class ImageClassifier:
    """
    Main image classification interface.

    Usage:
        classifier = ImageClassifier()
        result = classifier.classify(image_path)
    """

    def __init__(self):

        self.ai_classifier = ai_classifier
        self.feature_extractor = feature_extractor
        self.ocr_detector = ocr_detector
        self.decision_engine = decision_engine

    def classify(self, image_path):
        """
        Classify an image.

        Parameters
        ----------
        image_path : str | Path

        Returns
        -------
        dict
        """

        # ----------------------------------------
        # Step 1 : AI Prediction
        # ----------------------------------------

        ai_result = self.ai_classifier.predict_best(
            image_path
        )

        # ----------------------------------------
        # Step 2 : Extract Features
        # ----------------------------------------

        features = self.feature_extractor.extract(
            image_path
        )

        # ----------------------------------------
        # Step 3 : OCR
        # ----------------------------------------

        ocr_result = self.ocr_detector.detect(
            image_path
        )

        # ----------------------------------------
        # Step 4 : Final Decision
        # ----------------------------------------

        result = self.decision_engine.classify(
            ai_result=ai_result,
            features=features,
            ocr_result=ocr_result,
        )

        # ----------------------------------------
        # Include Additional Information
        # ----------------------------------------

        result["ai_prediction"] = ai_result

        result["features"] = features

        result["ocr"] = ocr_result

        return result


image_classifier = ImageClassifier()