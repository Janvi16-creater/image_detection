"""
Decision Engine

Combines outputs from OpenCV detectors.

If confidence is high enough,
OpenCV result is accepted.

Otherwise the classifier will
invoke Hugging Face.
"""


class DecisionEngine:

    def __init__(self):

        self.ai_threshold = 0.75

    # ---------------------------------------------------------

    def decide(
        self,
        wallpaper_result,
        camera_result,
        screenshot_result,
        widget_result=None,
        document_result=None,
    ):

        scores = {

            "wallpaper": wallpaper_result["confidence"],

            "camera": camera_result["confidence"],

            "screenshot": screenshot_result["confidence"],

            "widget": 0.0,

            "document": 0.0

        }

        # ---------------------------------------
        # Widget
        # ---------------------------------------

        if widget_result is not None:

            scores["widget"] = widget_result["confidence"]

        # ---------------------------------------
        # Document
        # ---------------------------------------

        if document_result is not None:

            scores["document"] = document_result["confidence"]

        # ---------------------------------------
        # Highest confidence
        # ---------------------------------------

        category = max(scores, key=scores.get)

        confidence = scores[category]

        # ---------------------------------------
        # Should AI be used?
        # ---------------------------------------

        use_ai = confidence < self.ai_threshold

        return {

            "category": category,

            "confidence": round(confidence, 3),

            "scores": scores,

            "use_ai": use_ai

        }

    # ---------------------------------------------------------

    def merge_ai_result(
        self,
        cv_result,
        ai_result
    ):
        """
        Merge OpenCV result with AI result.

        AI is trusted when OpenCV confidence
        is below the configured threshold.
        """

        if not cv_result["use_ai"]:

            return {

                "category": cv_result["category"],

                "confidence": cv_result["confidence"],

                "source": "opencv",

                "scores": cv_result["scores"]

            }

        return {

            "category": ai_result["category"],

            "confidence": ai_result["confidence"],

            "source": "huggingface",

            "prompt": ai_result["prompt"],

            "scores": ai_result["scores"]

        }


decision_engine = DecisionEngine()