"""
Screenshot Candidate Detector

This detector DOES NOT classify screenshots.

It only decides whether OCR should be executed.
"""


class ScreenshotDetector:

    def __init__(self):

        pass

    # ----------------------------------------------------------

    def detect(self, features):

        score = 0.0
        reasons = []

        # Many horizontal UI lines

        if features["horizontal_lines"] > 8:

            score += 0.25
            reasons.append("horizontal lines")

        # Many vertical UI lines

        if features["vertical_lines"] > 8:

            score += 0.20
            reasons.append("vertical lines")

        # Lots of edges

        if features["edge_density"] > 0.15:

            score += 0.20
            reasons.append("high edge density")

        # Strong center details

        if features["center_edge_density"] > 0.20:

            score += 0.20
            reasons.append("center details")

        # Portrait layout

        ratio = features["aspect_ratio"]

        if ratio < 0.70:

            score += 0.15
            reasons.append("portrait layout")

        confidence = min(score, 1.0)

        return {

            "candidate": confidence >= 0.55,

            "confidence": round(confidence, 2),

            "reason": ", ".join(reasons)

        }


screenshot_detector = ScreenshotDetector()