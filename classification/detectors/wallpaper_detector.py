"""
Wallpaper Detector

Determines how likely an image is a wallpaper
using OpenCV features.
"""


class WallpaperDetector:

    def detect(self, features):

        score = 0.0

        reasons = []

        # ----------------------------------------
        # Very few text regions
        # ----------------------------------------

        if features["text_boxes"] <= 2:
            score += 0.25
            reasons.append("very_few_text")

        elif features["text_boxes"] <= 5:
            score += 0.15

        # ----------------------------------------
        # Very few icons
        # ----------------------------------------

        if features["icon_count"] <= 2:
            score += 0.35
            reasons.append("no_icons")

        elif features["icon_count"] <= 5:
            score += 0.20

        # ----------------------------------------
        # No status bar
        # ----------------------------------------

        if features["top_density"] < 0.04:
            score += 0.15
            reasons.append("no_status_bar")

        # ----------------------------------------
        # No navigation bar
        # ----------------------------------------

        if features["bottom_density"] < 0.04:
            score += 0.15
            reasons.append("no_navigation_bar")

        # ----------------------------------------
        # Smooth image
        # ----------------------------------------

        if features["edge_density"] < 0.06:
            score += 0.10

        confidence = min(score, 1.0)

        return {

            "candidate": confidence >= 0.50,

            "confidence": round(confidence, 3),

            "reasons": reasons,

        }


wallpaper_detector = WallpaperDetector()