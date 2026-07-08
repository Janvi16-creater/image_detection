"""
Hybrid Image Classifier

Pipeline

Image
   │
   ├── Feature Extraction (OpenCV)
   ├── Screenshot Detector
   ├── Wallpaper Detector
   ├── Decision Engine
   │
   ├── High confidence?
   │      │
   │      ├── Yes → OpenCV Result
   │      └── No
   │
   └── SigLIP AI
"""

from classification.feature_extractor import feature_extractor
from classification.detectors.screenshot_detector import screenshot_detector
from classification.detectors.wallpaper_detector import wallpaper_detector
from classification.decision_engine import decision_engine
from classification.ai_classifier import ai_classifier


class ImageClassifier:

    def __init__(self):

        self.ai_threshold = 0.75

    # ---------------------------------------------------------

    def classify(self, image_path, image):

        # ----------------------------
        # OpenCV Features
        # ----------------------------

        features = feature_extractor.extract(image)

        screenshot = screenshot_detector.detect(features)

        wallpaper = wallpaper_detector.detect(features)

        # ----------------------------
        # Decision Engine
        # ----------------------------

        cv_result = decision_engine.decide(

            screenshot_result=screenshot,

            wallpaper_result=wallpaper

        )

        print("\n-------------------------------")
        print(image_path.name)
        print("Screenshot :", screenshot["confidence"])
        print("Wallpaper  :", wallpaper["confidence"])
        print("Decision   :", cv_result["category"])
        print("Confidence :", cv_result["confidence"])
        print("Use AI     :", cv_result["use_ai"])

        # ----------------------------
        # OpenCV confident enough
        # ----------------------------

        if not cv_result["use_ai"]:

            cv_result["source"] = "opencv"

            return cv_result

        # ----------------------------
        # AI Fallback
        # ----------------------------

        print("Running SigLIP...")

        ai_result = ai_classifier.classify(image_path)

        final = decision_engine.merge_ai_result(

            cv_result,

            ai_result

        )

        if "source" not in final:

            final["source"] = "opencv"

        return final


image_classifier = ImageClassifier()