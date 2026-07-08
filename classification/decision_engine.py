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

            }

        # -----------------------------------------
        # Wallpaper Slightly Better
        # -----------------------------------------

        return {

            "category": "wallpaper",

            "confidence": wallpaper_score,

            "source": "opencv",

            "use_ai": wallpaper_score < self.ai_threshold,

        }

    # -----------------------------------------------------

    def merge_ai_result(

        self,

        cv_result,

        ai_result,

    ):

        """
        AI overrides OpenCV only if sufficiently confident —
        UNLESS OpenCV had no opinion at all (category is None,
        the "very close scores" case). In that case OpenCV
        never had a real answer to fall back on, so AI's
        result is used regardless of its confidence; the
        alternative silently ships a blank/None category.
        """

        if cv_result.get("category") is None:

            return ai_result

        if ai_result["confidence"] >= 0.90:

            return ai_result

        return cv_result


decision_engine = DecisionEngine()