"""
Screenshot Detector

Verifies whether an image is likely to be
a screenshot using:

- AI prediction
- OCR information
- Image features

This module returns a confidence score rather
than a hard decision.
"""

from typing import Dict


class ScreenshotDetector:

    def __init__(self):

        self.mobile_ratios = [
            9 / 16,
            9 / 19.5,
            9 / 20,
            9 / 21
        ]

    def verify(
        self,
        ai_result: Dict,
        features: Dict,
        ocr_result: Dict,
    ):

        score = 0.0
        reasons = []

        # -----------------------------------
        # AI Prediction
        # -----------------------------------

        ai_scores = ai_result["scores"]

        mobile_score = ai_scores.get(
            "mobile screenshot",
            0
        )

        desktop_score = ai_scores.get(
            "desktop screenshot",
            0
        )

        ai_score = max(
            mobile_score,
            desktop_score
        )

        score += ai_score * 0.55

        if ai_score > 0.50:
            reasons.append(
                "AI strongly predicts screenshot"
            )

        # -----------------------------------
        # OCR
        # -----------------------------------

        text_count = ocr_result["text_count"]

        if text_count >= 20:

            score += 0.15

            reasons.append(
                "large amount of text detected"
            )

        elif text_count >= 10:

            score += 0.10

            reasons.append(
                "moderate amount of text"
            )

        text_density = ocr_result["text_density"]

        if text_density > 0.12:

            score += 0.10

            reasons.append(
                "high text density"
            )

        # -----------------------------------
        # Edge Density
        # -----------------------------------

        if features["edge_density"] > 0.10:

            score += 0.08

            reasons.append(
                "high edge density"
            )

        # -----------------------------------
        # Entropy
        # -----------------------------------

        if features["entropy"] > 6:

            score += 0.04

            reasons.append(
                "high visual complexity"
            )

        # -----------------------------------
        # Contrast
        # -----------------------------------

        if features["contrast"] > 0.18:

            score += 0.03

            reasons.append(
                "good contrast"
            )

        # -----------------------------------
        # Aspect Ratio
        # -----------------------------------

        ratio = features["aspect_ratio"]

        portrait = min(
            abs(ratio - r)
            for r in self.mobile_ratios
        )

        if portrait < 0.05:

            score += 0.05

            reasons.append(
                "mobile aspect ratio"
            )

        elif ratio > 1.3:

            score += 0.04

            reasons.append(
                "desktop aspect ratio"
            )

        # -----------------------------------
        # Final Score
        # -----------------------------------

        score = min(score, 1.0)

        return {

            "category": "screenshot",

            "confidence": round(score, 4),

            "verified": score >= 0.60,

            "reasons": reasons

        }


screenshot_detector = ScreenshotDetector()