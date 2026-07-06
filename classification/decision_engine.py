"""
Decision Engine

This module combines all detector outputs and
returns the final image category.

Priority:
1. Screenshot
2. Document
3. Widget
4. Wallpaper
5. Camera Photo
"""

from classification.detectors.document_detector import document_detector
from classification.detectors.screenshot_detector import screenshot_detector
from classification.detectors.wallpaper_detector import wallpaper_detector
from classification.detectors.widget_detector import widget_detector


class DecisionEngine:

    def __init__(self):

        self.threshold = 0.60

    def classify(
        self,
        ai_result,
        features,
        ocr_result,
    ):
        """
        Returns
        -------
        dict

        {
            category,
            confidence,
            detector_scores,
            reasons
        }
        """

        screenshot = screenshot_detector.verify(
            ai_result,
            features,
            ocr_result,
        )

        wallpaper = wallpaper_detector.verify(
            ai_result,
            features,
            ocr_result,
        )

        widget = widget_detector.verify(
            ai_result,
            features,
            ocr_result,
        )

        document = document_detector.verify(
            ai_result,
            features,
            ocr_result,
        )

        detector_results = {

            "screenshot": screenshot,

            "wallpaper": wallpaper,

            "widget": widget,

            "document": document,

        }

        # --------------------------------------------------
        # Pick detector having highest confidence
        # --------------------------------------------------

        best_category = None

        best_result = None

        best_score = 0

        for category, result in detector_results.items():

            if result["confidence"] > best_score:

                best_score = result["confidence"]

                best_category = category

                best_result = result

        # --------------------------------------------------
        # If detector confidence is sufficient
        # --------------------------------------------------

        if best_score >= self.threshold:

            return {

                "category": best_category,

                "confidence": round(best_score, 4),

                "reason": best_result["reasons"],

                "detector_scores": {

                    name: round(
                        value["confidence"],
                        4,
                    )

                    for name, value in detector_results.items()

                }

            }

        # --------------------------------------------------
        # Otherwise use AI prediction
        # --------------------------------------------------

        ai_category = ai_result["category"]

        if ai_category == "mobile screenshot":
            final_category = "screenshot"

        elif ai_category == "desktop screenshot":
            final_category = "screenshot"

        elif ai_category == "application widget":
            final_category = "widget"

        elif ai_category == "camera photograph":
            final_category = "camera_photo"

        else:
            final_category = ai_category

        return {

            "category": final_category,

            "confidence": ai_result["confidence"],

            "reason": [

                "No detector exceeded threshold.",
                "Using AI prediction."

            ],

            "detector_scores": {

                name: round(
                    value["confidence"],
                    4,
                )

                for name, value in detector_results.items()

            }

        }


decision_engine = DecisionEngine()

#                   AI Prediction
#                        │
#                        ▼
#              Feature Extraction
#                        │
#                        ▼
#                  OCR Detection
#                        │
#                        ▼
#         ┌──────────────┼──────────────┐
#         ▼              ▼              ▼
#  Screenshot      Wallpaper      Widget
#         │
#         ▼
#    Document Detector
#         │
#         ▼
#      Decision Engine
#         │
#         ▼
#  Highest Confidence Wins
#         │
#         ▼
#  Final Category