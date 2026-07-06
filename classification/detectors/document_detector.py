"""
Document Detector

Verifies whether an image is likely to be
a document.

Supports:
- PDF pages
- Scanned documents
- Notes
- Books
- Bills
- Certificates
- Forms
"""

from typing import Dict


class DocumentDetector:

    def __init__(self):
        pass

    def verify(
        self,
        ai_result: Dict,
        features: Dict,
        ocr_result: Dict,
    ):

        score = 0.0
        reasons = []

        # ------------------------------------
        # AI Prediction
        # ------------------------------------

        ai_score = ai_result["scores"].get(
            "document",
            0
        )

        score += ai_score * 0.55

        if ai_score > 0.50:

            reasons.append(
                "AI strongly predicts document"
            )

        # ------------------------------------
        # OCR Text Count
        # ------------------------------------

        text_count = ocr_result["text_count"]

        if text_count > 40:

            score += 0.15

            reasons.append(
                "large amount of text"
            )

        elif text_count > 20:

            score += 0.10

            reasons.append(
                "moderate amount of text"
            )

        # ------------------------------------
        # Total Characters
        # ------------------------------------

        characters = ocr_result["total_characters"]

        if characters > 500:

            score += 0.10

            reasons.append(
                "large amount of readable content"
            )

        elif characters > 250:

            score += 0.05

            reasons.append(
                "medium amount of readable content"
            )

        # ------------------------------------
        # OCR Density
        # ------------------------------------

        density = ocr_result["text_density"]

        if density > 0.20:

            score += 0.08

            reasons.append(
                "high text density"
            )

        # ------------------------------------
        # Brightness
        # ------------------------------------

        brightness = features["brightness"]

        if brightness > 0.65:

            score += 0.05

            reasons.append(
                "bright background"
            )

        # ------------------------------------
        # Saturation
        # ------------------------------------

        saturation = features["saturation"]

        if saturation < 0.20:

            score += 0.05

            reasons.append(
                "low saturation"
            )

        # ------------------------------------
        # Contrast
        # ------------------------------------

        contrast = features["contrast"]

        if contrast > 0.15:

            score += 0.03

            reasons.append(
                "good text contrast"
            )

        # ------------------------------------
        # Edge Density
        # ------------------------------------

        edge_density = features["edge_density"]

        if 0.05 <= edge_density <= 0.15:

            score += 0.03

            reasons.append(
                "moderate edge density"
            )

        # ------------------------------------
        # Entropy
        # ------------------------------------

        entropy = features["entropy"]

        if entropy > 6:

            score += 0.02

            reasons.append(
                "high information content"
            )

        # ------------------------------------
        # Final Score
        # ------------------------------------

        score = max(
            0.0,
            min(score, 1.0)
        )

        return {

            "category": "document",

            "confidence": round(score, 4),

            "verified": score >= 0.60,

            "reasons": reasons

        }


document_detector = DocumentDetector()