"""
Wallpaper Detector

Detects wallpaper/background images using
visual features extracted from FeatureExtractor.
"""


class WallpaperDetector:

    def __init__(self):

        pass

    # ----------------------------------------------------------

    def detect(self, features):

        score = 0.0
        reasons = []

        # Large image
        if features["megapixels"] >= 1:
            score += 0.10
            reasons.append("large image")

        # Smooth image
        if features["edge_density"] < 0.08:
            score += 0.30
            reasons.append("low edge density")

        # Low texture
        if features["entropy"] < 6.5:
            score += 0.20
            reasons.append("low entropy")

        # Soft contrast
        if features["contrast"] < 60:
            score += 0.15
            reasons.append("low contrast")

        # Rich colors
        if features["saturation"] > 60:
            score += 0.10
            reasons.append("good saturation")

        # Few straight UI lines
        if (
            features["horizontal_lines"] < 8
            and
            features["vertical_lines"] < 8
        ):
            score += 0.15
            reasons.append("few UI lines")

        confidence = min(score, 1.0)

        return {

            "is_wallpaper": confidence >= 0.70,

            "confidence": round(confidence, 2),

            "reason": ", ".join(reasons)

        }


wallpaper_detector = WallpaperDetector()