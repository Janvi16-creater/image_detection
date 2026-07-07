"""
Camera Photo Detector

Detects natural photographs.

Examples:
- Selfies
- Landscape
- Food
- Animals
- People
"""


class CameraDetector:

    def __init__(self):

        pass

    # ----------------------------------------------------------

    def detect(self, features):

        score = 0.0
        reasons = []

        # Natural photos usually contain
        # many edges

        if features["edge_density"] > 0.12:

            score += 0.25
            reasons.append("many edges")

        # Rich information

        if features["entropy"] > 7:

            score += 0.20
            reasons.append("high entropy")

        # Natural contrast

        if features["contrast"] > 50:

            score += 0.15
            reasons.append("good contrast")

        # Strong color variation

        if features["color_variance"] > 2000:

            score += 0.20
            reasons.append("rich colors")

        # Sharp image

        if features["sharpness"] > 150:

            score += 0.20
            reasons.append("sharp image")

        confidence = min(score, 1.0)

        return {

            "is_camera": confidence >= 0.75,

            "confidence": round(confidence, 2),

            "reason": ", ".join(reasons)

        }


camera_detector = CameraDetector()