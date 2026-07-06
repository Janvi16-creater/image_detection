"""
Wallpaper Detector

Verifies whether an image is likely to be
a wallpaper.

Uses:

- AI Prediction
- OCR
- Edge Density
- Saturation
- Brightness
- Contrast
- Entropy
"""

from typing import Dict


class WallpaperDetector:

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

        # ---------------------------------------
        # AI Prediction
        # ---------------------------------------

        ai_score = ai_result["scores"].get(
            "wallpaper",
            0
        )

        score += ai_score * 0.60

        if ai_score > 0.50:

            reasons.append(
                "AI strongly predicts wallpaper"
            )

        # ---------------------------------------
        # OCR
        # ---------------------------------------

        text_count = ocr_result["text_count"]

        if text_count == 0:

            score += 0.12

            reasons.append(
                "no text detected"
            )

        elif text_count < 5:

            score += 0.06

            reasons.append(
                "very little text"
            )

        else:

            score -= 0.10

            reasons.append(
                "large amount of text detected"
            )

        # ---------------------------------------
        # Edge Density
        # ---------------------------------------

        edge_density = features["edge_density"]

        if edge_density < 0.05:

            score += 0.08

            reasons.append(
                "low edge density"
            )

        elif edge_density > 0.15:

            score -= 0.05

            reasons.append(
                "too many edges"
            )

        # ---------------------------------------
        # Saturation
        # ---------------------------------------

        saturation = features["saturation"]

        if saturation > 0.30:

            score += 0.05

            reasons.append(
                "rich colors"
            )

        # ---------------------------------------
        # Brightness
        # ---------------------------------------

        brightness = features["brightness"]

        if 0.25 <= brightness <= 0.85:

            score += 0.03

            reasons.append(
                "balanced brightness"
            )

        # ---------------------------------------
        # Contrast
        # ---------------------------------------

        contrast = features["contrast"]

        if contrast < 0.22:

            score += 0.04

            reasons.append(
                "low contrast"
            )

        # ---------------------------------------
        # Entropy
        # ---------------------------------------

        entropy = features["entropy"]

        if entropy < 6.5:

            score += 0.03

            reasons.append(
                "simple visual texture"
            )

        # ---------------------------------------
        # Resolution Bonus
        # ---------------------------------------

        width = features["width"]
        height = features["height"]

        if max(width, height) >= 1080:

            score += 0.05

            reasons.append(
                "high resolution"
            )

        # ---------------------------------------
        # Final Score
        # ---------------------------------------

        score = max(
            0.0,
            min(score, 1.0)
        )

        return {

            "category": "wallpaper",

            "confidence": round(score, 4),

            "verified": score >= 0.60,

            "reasons": reasons

        }


wallpaper_detector = WallpaperDetector()