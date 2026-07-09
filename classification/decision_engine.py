"""
Decision Engine

Combines OpenCV detectors and
uses AI only when necessary.
"""


class DecisionEngine:

    def __init__(self):

        # AI will only be used when
        # confidence is low.
        self.ai_threshold = 0.70

    # -----------------------------------------------------

    def decide(

        self,

        screenshot_result,

        wallpaper_result

    ):

        screenshot_score = screenshot_result["confidence"]
        wallpaper_score = wallpaper_result["confidence"]

        # -----------------------------------------
        # Strong Screenshot
        # -----------------------------------------

        if screenshot_score >= 0.75 and screenshot_score > wallpaper_score:

            return {

                "category": "screenshot",

                "confidence": screenshot_score,

                "source": "opencv",

                "use_ai": False,

                "screenshot_score": screenshot_score,

                "wallpaper_score": wallpaper_score,

            }

        # -----------------------------------------
        # Strong Wallpaper
        # -----------------------------------------

        if wallpaper_score >= 0.75 and wallpaper_score > screenshot_score:

            return {

                "category": "wallpaper",

                "confidence": wallpaper_score,

                "source": "opencv",

                "use_ai": False,

                "screenshot_score": screenshot_score,

                "wallpaper_score": wallpaper_score,

            }

        # -----------------------------------------
        # Very Close Scores
        # -----------------------------------------

        difference = abs(
            screenshot_score -
            wallpaper_score
        )

        if difference < 0.20:

            return {

                "category": None,

                "confidence": max(
                    screenshot_score,
                    wallpaper_score,
                ),

                "source": "opencv",

                "use_ai": True,

                "screenshot_score": screenshot_score,

                "wallpaper_score": wallpaper_score,

            }

        # -----------------------------------------
        # Screenshot Slightly Better
        # -----------------------------------------

        if screenshot_score > wallpaper_score:

            return {

                "category": "screenshot",

                "confidence": screenshot_score,

                "source": "opencv",

                "use_ai": screenshot_score < self.ai_threshold,

                "screenshot_score": screenshot_score,

                "wallpaper_score": wallpaper_score,

            }

        # -----------------------------------------
        # Wallpaper Slightly Better
        # -----------------------------------------

        return {

            "category": "wallpaper",

            "confidence": wallpaper_score,

            "source": "opencv",

            "use_ai": wallpaper_score < self.ai_threshold,

            "screenshot_score": screenshot_score,

            "wallpaper_score": wallpaper_score,

        }

    # -----------------------------------------------------

    def re_decide(self, cv_result, gemini_result):
        """
        Re-evaluate using both OpenCV scores and Gemini scene context.

        Gemini's scene understanding (has_ui_elements, scene_type) can
        override OpenCV when OpenCV was uncertain. Gemini's enriched
        fields (description, orientation, scene_type, etc.) are always
        merged into the final result.

        Priority:
        1. Gemini confidence >= 0.90 → full trust in Gemini
        2. Gemini says has_ui_elements → screenshot
        3. Gemini says no UI + natural scene → wallpaper
        4. Otherwise → keep OpenCV's verdict
        """
        if gemini_result.get("category") is None:
            return cv_result

        if gemini_result.get("confidence", 0) >= 0.90:
            return gemini_result

        result = dict(cv_result)
        result["source"] = "opencv+gemini"

        if gemini_result.get("has_ui_elements", False):
            result["category"] = "screenshot"
            result["confidence"] = round(max(
                result.get("confidence", 0),
                gemini_result.get("confidence", 0),
            ), 3)

        elif gemini_result.get("scene_type") in ("photo", "artwork", "abstract"):
            result["category"] = "wallpaper"
            result["confidence"] = round(max(
                result.get("confidence", 0),
                gemini_result.get("confidence", 0),
            ), 3)

        result["has_ui_elements"] = gemini_result.get("has_ui_elements", False)
        result["orientation"] = gemini_result.get("orientation", "unknown")
        result["scene_type"] = gemini_result.get("scene_type", "")
        result["wallpaper_suitable"] = gemini_result.get("wallpaper_suitable", False)
        result["wallpaper_reason"] = gemini_result.get("wallpaper_reason", "")
        result["description"] = gemini_result.get("description", "")

        return result


decision_engine = DecisionEngine()