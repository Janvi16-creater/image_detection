"""
Hybrid Image Classifier

Pipeline

Image
│
├── Feature Extraction
│
├── Wallpaper Detector
│
├── Camera Detector
│
├── Screenshot Detector
│
├── OCR (Only if Screenshot Candidate)
│
├── Widget Detector
│
├── Document Detector
│
├── Decision Engine
│
├── Confidence >= Threshold ?
│        │
│        ├── YES → OpenCV Result
│        │
│        └── NO
│             │
│             ▼
│      HuggingFace SigLIP
│             │
│             ▼
│      AI Stronger ?
│             │
│      Yes → AI Result
│      No  → OpenCV Result
"""

from classification.feature_extractor import feature_extractor

from classification.detectors.wallpaper_detector import wallpaper_detector
from classification.detectors.camera_detector import camera_detector
from classification.detectors.screenshot_detector import screenshot_detector
from classification.detectors.widget_detector import widget_detector
from classification.detectors.document_detector import document_detector

from classification.ocr_detector import ocr_detector

from classification.ai.ai_classifier import ai_classifier

from classification.decision_engine import decision_engine


class ImageClassifier:

    def __init__(self):

        self.ai_margin = 0.15
        self.ai_min_confidence = 0.75

    # -------------------------------------------------------------

    def classify(self, image_path, image):

        # ---------------------------------------------------------
        # Feature Extraction
        # ---------------------------------------------------------

        features = feature_extractor.extract(image)

        # ---------------------------------------------------------
        # Fast OpenCV Detectors
        # ---------------------------------------------------------

        wallpaper_result = wallpaper_detector.detect(features)

        camera_result = camera_detector.detect(features)

        screenshot_result = screenshot_detector.detect(features)

        widget_result = None
        document_result = None

        # ---------------------------------------------------------
        # OCR (Only for Screenshot Candidates)
        # ---------------------------------------------------------

        if screenshot_result["candidate"]:

            ocr_result = ocr_detector.detect(image_path)

            widget_result = widget_detector.detect(
                features,
                ocr_result
            )

            document_result = document_detector.detect(
                features,
                ocr_result
            )

        # ---------------------------------------------------------
        # OpenCV Decision
        # ---------------------------------------------------------

        cv_result = decision_engine.decide(

            wallpaper_result=wallpaper_result,

            camera_result=camera_result,

            screenshot_result=screenshot_result,

            widget_result=widget_result,

            document_result=document_result

        )

        # ---------------------------------------------------------
        # Debug
        # ---------------------------------------------------------

        print("\n" + "=" * 70)

        print(image_path.name)

        print("Wallpaper :", wallpaper_result["confidence"])
        print("Camera    :", camera_result["confidence"])
        print("Screenshot:", screenshot_result["confidence"])

        if widget_result:
            print("Widget    :", widget_result["confidence"])

        if document_result:
            print("Document  :", document_result["confidence"])

        print("Decision  :", cv_result["category"])
        print("Confidence:", cv_result["confidence"])
        print("Use AI    :", cv_result["use_ai"])

        # ---------------------------------------------------------
        # OpenCV is already confident
        # ---------------------------------------------------------

        if not cv_result["use_ai"]:

            return {

                "category": cv_result["category"],

                "confidence": cv_result["confidence"],

                "source": "opencv"

            }

        # ---------------------------------------------------------
        # AI Fallback
        # ---------------------------------------------------------

        print("Running HuggingFace...")

        ai_result = ai_classifier.classify(image_path)

        print(
            "AI Result :",
            ai_result["category"],
            ai_result["confidence"]
        )

        # ---------------------------------------------------------
        # AI overrides only if clearly stronger
        # ---------------------------------------------------------

        if (

            ai_result["confidence"] >= self.ai_min_confidence

            and

            ai_result["confidence"] >
            cv_result["confidence"] + self.ai_margin

        ):

            print("Final     : AI")

            return {

                "category": ai_result["category"],

                "confidence": ai_result["confidence"],

                "source": "huggingface"

            }

        # ---------------------------------------------------------
        # Otherwise keep OpenCV
        # ---------------------------------------------------------

        print("Final     : OpenCV")

        return {

            "category": cv_result["category"],

            "confidence": cv_result["confidence"],

            "source": "opencv"

        }


image_classifier = ImageClassifier()