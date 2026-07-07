"""
Widget Detector

Detects app widgets and UI screenshots.

Uses OCR + OpenCV Features.
"""


class WidgetDetector:

    def detect(self, features, ocr_result):

        score = 0.0
        reasons = []

        word_count = ocr_result["word_count"]

        # --------------------------------------------------
        # OCR
        # --------------------------------------------------

        # Widgets can contain a moderate amount of text

        if word_count <= 15:

            score += 0.15

        elif word_count <= 60:

            score += 0.20
            reasons.append("normal UI text")

        elif word_count <= 100:

            score += 0.10

        # --------------------------------------------------
        # Dense UI

        if features["center_edge_density"] > 0.20:

            score += 0.20
            reasons.append("dense UI")

        # Many edges

        if features["edge_density"] > 0.15:

            score += 0.15

        # UI contains many horizontal separators

        if features["horizontal_lines"] >= 10:

            score += 0.15

        # UI contains many vertical separators

        if features["vertical_lines"] >= 6:

            score += 0.15

        # Portrait screenshots

        ratio = features["aspect_ratio"]

        if ratio < 0.80:

            score += 0.10

        # Sharp UI

        if features["sharpness"] > 180:

            score += 0.10

        confidence = min(score, 1.0)

        return {

            "is_widget": confidence >= 0.70,

            "confidence": round(confidence, 2),

            "reason": ", ".join(reasons)

        }


widget_detector = WidgetDetector()