"""
Document Detector

Detects:
- PDF
- Book
- Notes
- Receipt
- Scanned Paper

Uses BOTH OCR and image features.
"""

import re


class DocumentDetector:

    def detect(self, features, ocr_result):

        words = ocr_result.get("text", [])
        word_count = ocr_result.get("word_count", 0)

        score = 0.0
        reasons = []

        # --------------------------------------------------
        # OCR
        # --------------------------------------------------

        if word_count > 120:
            score += 0.30
            reasons.append("very high word count")

        elif word_count > 70:
            score += 0.20
            reasons.append("high word count")

        elif word_count > 40:
            score += 0.10

        characters = sum(len(w) for w in words)

        if characters > 600:
            score += 0.20
            reasons.append("high text density")

        # --------------------------------------------------
        # Mostly alphabetic text
        # --------------------------------------------------

        alphabetic = sum(
            1
            for w in words
            if re.fullmatch(r"[A-Za-z]+", w)
        )

        if word_count:

            ratio = alphabetic / word_count

            if ratio > 0.80:
                score += 0.10
                reasons.append("clean readable text")

        # --------------------------------------------------
        # OpenCV Features
        # --------------------------------------------------

        # Documents usually have fewer edges

        if features["edge_density"] < 0.10:
            score += 0.15
            reasons.append("few edges")

        # Documents have fewer UI lines

        if features["horizontal_lines"] < 8:
            score += 0.05

        if features["vertical_lines"] < 8:
            score += 0.05

        # White backgrounds are common

        if features["brightness"] > 180:
            score += 0.10
            reasons.append("bright background")

        confidence = min(score, 1.0)

        return {

            "is_document": confidence >= 0.75,

            "confidence": round(confidence, 2),

            "reason": ", ".join(reasons)

        }


document_detector = DocumentDetector()