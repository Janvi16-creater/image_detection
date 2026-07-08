"""
UI Detector

Determines how likely an image is a screenshot
based on UI-related OpenCV features.
"""


class UIDetector:

    def detect(self, features):

        score = 0.0

        reasons = []

        # ----------------------------------------
        # Text Regions
        # ----------------------------------------

        if features["text_boxes"] >= 12:
            score += 0.25
            reasons.append("many_text_regions")

        elif features["text_boxes"] >= 6:
            score += 0.15

        # ----------------------------------------
        # App Icons
        # ----------------------------------------

        if features["icon_count"] >= 10:
            score += 0.30
            reasons.append("many_icons")

        elif features["icon_count"] >= 5:
            score += 0.20

        # ----------------------------------------
        # Status Bar
        # ----------------------------------------

        if features["top_density"] >= 0.06:
            score += 0.20
            reasons.append("status_bar")

        # ----------------------------------------
        # Navigation Bar / Dock
        # ----------------------------------------

        if features["bottom_density"] >= 0.05:
            score += 0.15
            reasons.append("navigation_bar")

        # ----------------------------------------
        # Overall Edge Density
        # ----------------------------------------

        if features["edge_density"] >= 0.08:
            score += 0.10

        confidence = min(score, 1.0)

        return {

            "candidate": confidence >= 0.50,

            "confidence": round(confidence, 3),

            "reasons": reasons,

        }


ui_detector = UIDetector()