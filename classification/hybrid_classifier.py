"""
Hybrid Classifier

Two-stage classification:
1. OpenCV heuristics — cheap pre-filter for obvious cases
2. Gemini API — for uncertain cases (handles rate limiting internally)

Classifier determines whether an image is a "screenshot" or "wallpaper".
If Gemini is unavailable or fails, OpenCV's verdict is used as fallback
so every image is always classified — no "unknown" results.
"""

import cv2

from classification.feature_extractor import feature_extractor
from classification.detectors.screenshot_detector import screenshot_detector
from classification.detectors.wallpaper_detector import wallpaper_detector
from classification.decision_engine import decision_engine
from classification.ai_classifier import ai_classifier


def _force_opencv_decision(cv_result):
    """
    If OpenCV couldn't decide (category is None), force a decision.

    When both scores are low (< 0.5) and close, prefer wallpaper —
    images with no real UI signals (icons, widgets, grid) are more
    likely to be detail-rich wallpapers than screenshots.
    """
    if cv_result.get("category") is not None:
        return cv_result

    ss = cv_result.get("screenshot_score", 0)
    wp = cv_result.get("wallpaper_score", 0)

    if abs(ss - wp) < 0.10 and max(ss, wp) < 0.5:
        cv_result["category"] = "wallpaper"
    elif ss >= wp:
        cv_result["category"] = "screenshot"
    else:
        cv_result["category"] = "wallpaper"

    return cv_result


def _enrich_cv_result(cv_result, features, wallpaper_result):
    """Add derived fields aligned with the final category decision."""
    h = features.get("height", 0)
    w = features.get("width", 0)

    if w > 0 and h > 0:
        ratio = w / h
        if ratio > 1.1:
            orientation = "landscape"
        elif ratio < 0.9:
            orientation = "portrait"
        else:
            orientation = "square"
    else:
        orientation = "unknown"

    icon_count = features.get("icon_count", 0)
    text_regions = features.get("text_regions", 0)
    grid_score = features.get("grid_score", 0)
    category = cv_result.get("category", "wallpaper")

    if category == "screenshot":
        has_ui = True
        if grid_score > 0.3:
            scene_type = "phone_home_screen"
        else:
            scene_type = "app_screen"
        wallpaper_suitable = False
        wallpaper_reason = "Contains UI elements"
        parts = [f"{w}x{h}", f"{icon_count} icons, {text_regions} text regions"]
    else:
        has_ui = False
        if features.get("edge_density", 0) > 0.08:
            scene_type = "photo"
        else:
            scene_type = "abstract"
        reasons = wallpaper_result.get("reasons", [])
        wallpaper_suitable = True
        wallpaper_reason = "; ".join(reasons) if reasons else "No UI elements detected"
        parts = [f"{w}x{h}"]

    description = ", ".join(parts)

    result = dict(cv_result)
    result.update({
        "orientation": orientation,
        "has_ui_elements": has_ui,
        "scene_type": scene_type,
        "wallpaper_suitable": wallpaper_suitable,
        "wallpaper_reason": wallpaper_reason,
        "description": description,
    })
    return result


class HybridClassifier:

    def classify(self, image_path):

        image = cv2.imread(str(image_path))

        if image is None:
            raise ValueError(f"Unable to read image: {image_path}")

        features = feature_extractor.extract(image)

        screenshot_result = screenshot_detector.detect(features)
        wallpaper_result = wallpaper_detector.detect(features)

        cv_result = decision_engine.decide(
            screenshot_result,
            wallpaper_result,
        )

        # OpenCV confident enough — skip Gemini
        if not cv_result["use_ai"]:
            return _enrich_cv_result(
                _force_opencv_decision(cv_result),
                features, wallpaper_result,
            )

        # OpenCV uncertain — use Gemini
        gemini_result = ai_classifier.classify(image_path)

        if gemini_result.get("category") is not None:
            return gemini_result

        return _enrich_cv_result(
            _force_opencv_decision(cv_result),
            features, wallpaper_result,
        )

    def classify_many(self, image_paths):
        """
        Classify multiple images.

        OpenCV runs on every image as a pre-filter. Images that
        OpenCV is confident about skip Gemini. The rest go to
        Gemini. If Gemini fails (rate limited, etc.), OpenCV's
        verdict is used as fallback — every image gets classified
        as "screenshot" or "wallpaper", never "unknown".
        """
        opencv_results = {}
        gemini_candidates = []

        for image_path in image_paths:
            image = cv2.imread(str(image_path))

            if image is None:
                opencv_results[image_path] = {
                    "category": "wallpaper",
                    "confidence": 0.0,
                    "source": "opencv_fallback",
                }
                continue

            features = feature_extractor.extract(image)
            screenshot_result = screenshot_detector.detect(features)
            wallpaper_result = wallpaper_detector.detect(features)

            cv_result = decision_engine.decide(
                screenshot_result,
                wallpaper_result,
            )
            cv_result = _force_opencv_decision(cv_result)
            cv_result = _enrich_cv_result(cv_result, features, wallpaper_result)

            # Store OpenCV result for each image (will use as fallback)
            opencv_results[image_path] = cv_result

            if cv_result["use_ai"]:
                gemini_candidates.append(image_path)

        # Send uncertain images to Gemini
        if gemini_candidates:
            print(
                f"\nOpenCV decided {len(opencv_results) - len(gemini_candidates)}/"
                f"{len(image_paths)} images, sending {len(gemini_candidates)} "
                f"to Gemini..."
            )
            gemini_results = ai_classifier.classify_many(gemini_candidates)
        else:
            gemini_results = {}

        # Merge: Gemini overrides OpenCV only when it succeeds
        final_results = dict(opencv_results)
        for path, gemini_result in gemini_results.items():
            if gemini_result.get("category") is not None:
                final_results[path] = gemini_result
            # else: keep OpenCV's decision as fallback

        return final_results


hybrid_classifier = HybridClassifier()
