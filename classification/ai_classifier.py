"""
AI Classifier using Gemini

Classifies images as screenshot or wallpaper, determines wallpaper
suitability, and extracts descriptive information.

Uses rate-limited sequential requests with exponential backoff
and model fallback to maximize free-tier API availability.
"""

import re
import time
import threading
from typing import Literal

from PIL import Image
from google import genai
from google.genai import types
from google.genai import errors as genai_errors
from pydantic import BaseModel

from config import GEMINI_API_KEY
from pathlib import Path
import hashlib
import random

# ---------------------------------------------------------------
# Development mode
# ---------------------------------------------------------------

USE_MOCK_GEMINI = False

# ---------------------------------------------------------------
# Structured output schema
# ---------------------------------------------------------------

class ClassificationResult(BaseModel):
    category: Literal["screenshot", "wallpaper"]
    confidence: float
    has_ui_elements: bool
    orientation: Literal["portrait", "landscape", "square", "unknown"]
    wallpaper_suitable: bool
    wallpaper_reason: str
    description: str
    scene_type: Literal[
        "phone_home_screen", "app_screen", "lock_screen",
        "settings_page", "browser_page", "desktop_ui",
        "photo", "artwork", "abstract", "other"
    ]


PROMPT = """
You are analyzing an image to classify it and assess wallpaper suitability.

First, determine if this is a "screenshot" or a "wallpaper":

"screenshot" means: any image of a device's user interface — phone home
screens, lock screens, app menus, browser windows, desktop screenshots,
software interfaces. Look for small UI giveaways: status bar (time,
battery, wifi), app icons in a grid, widgets, navigation bars, menu text,
or any on-screen controls.

"wallpaper" means: a photograph, illustration, artwork, or abstract image
with NO operating system UI elements. Even if it looks like it COULD be
used as a wallpaper background, if there are no UI elements it is a
"wallpaper".

Important: A lock screen with a nature photo background is still a
"screenshot" because it has UI elements (clock, notifications, etc.).

Next, assess wallpaper suitability:
- A wallpaper is suitable if it has NO text overlays, NO watermarks,
  NO UI elements, and good visual composition.
- Even beautiful photos with text/watermarks are NOT suitable wallpapers.

Next, classify the scene type:
- "phone_home_screen": phone/tablet home screen with icon grid
- "app_screen": any app interface (settings, messages, gallery, etc.)
- "lock_screen": device lock screen with clock/notifications
- "settings_page": system settings or configuration screen
- "browser_page": web browser or document
- "desktop_ui": computer desktop (Windows/Mac/Linux taskbar + windows)
- "photo": real-world photograph with no UI
- "artwork": digital art, painting, illustration
- "abstract": abstract patterns, gradients, solid colors
- "other": anything that doesn't fit above

Respond with:
- category: "screenshot" or "wallpaper"
- confidence: 0.0 to 1.0
- has_ui_elements: true if any UI elements are visible
- orientation: image orientation (portrait, landscape, square, or unknown)
- scene_type: one of the scene types above
- wallpaper_suitable: true if this image would make a good wallpaper
- wallpaper_reason: one sentence explaining why or why not
- description: brief description of the image content (10-20 words)
"""


# ---------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------

class RateLimiter:
    """
    Token-bucket rate limiter — ensures we never exceed max_calls
    per period seconds. Thread-safe.
    """

    def __init__(self, max_calls=8, period=60):
        self.max_calls = max_calls
        self.period = period
        self.timestamps = []
        self.lock = threading.Lock()

    def wait(self):
        with self.lock:
            now = time.time()
            cutoff = now - self.period
            self.timestamps = [t for t in self.timestamps if t > cutoff]
            if len(self.timestamps) >= self.max_calls:
                sleep_time = self.timestamps[0] + self.period - now
                if sleep_time > 0:
                    time.sleep(sleep_time)
            self.timestamps.append(time.time())


# ---------------------------------------------------------------
# AI Classifier
# ---------------------------------------------------------------

RETRYABLE_CODES = (429, 500, 503)


def _extract_retry_delay(error):
    """
    Extract retry delay from a 429 error response.

    The server sends retryDelay in JSON-like format with quoted
    values (e.g., ``'retryDelay': '12s'``).  The regex allows
    optional quotes around the numeric value.
    """
    try:
        raw = str(error)
        match = re.search(
            r"retry(?:Delay|_delay)\s*['\"]?\s*:\s*['\"]?(\d+(?:\.\d+)?)['\"]?\s*s",
            raw,
            re.IGNORECASE,
        )
        if match:
            return min(float(match.group(1)), 120)
    except Exception:
        pass

    return None


class AIClassifier:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        # gemini-2.0-flash: 1500 RPD free tier
        self.model = "gemini-2.5-flash"
        # gemini-2.0-flash: fallback (20 RPD, cheaper)
        self.fallback_model = None
        self.rate_limiter = RateLimiter(max_calls=5, period=60)

    # -----------------------------------------------------------
    
    def _is_daily_quota_exceeded(self, error):
        """
        Detect daily quota exhaustion.

        Daily quota errors should NOT be retried because waiting
        will not help until quota resets.
        """
        message = str(error)

        return (
            "GenerateRequestsPerDayPerProjectPerModel" in message
            or (
                "limit: 0" in message
                and "RESOURCE_EXHAUSTED" in message
            )
        )

    def _format_result(self, result):
        return {
            "category": result.category,
            "confidence": round(result.confidence, 3),
            "source": "gemini",
            "has_ui_elements": result.has_ui_elements,
            "orientation": result.orientation,
            "scene_type": result.scene_type,
            "wallpaper_suitable": result.wallpaper_suitable,
            "wallpaper_reason": result.wallpaper_reason,
            "description": result.description,
            "prompt": result.wallpaper_reason,
        }

    def _error_result(self, message):
        return {
            "category": None,
            "confidence": 0.0,
            "source": "gemini",
            "has_ui_elements": False,
            "orientation": "unknown",
            "scene_type": "",
            "wallpaper_suitable": False,
            "wallpaper_reason": message,
            "description": "",
            "prompt": message,
        }

    def _get_wait_time(self, attempt, error=None):
        """
        Return wait time in seconds.

        Uses the API's suggested retry delay for 429 errors if
        available; otherwise falls back to exponential backoff.
        """
        if error is not None:
            delay = _extract_retry_delay(error)
            if delay is not None:
                return min(delay, 120)
        return min(float(2 ** attempt), 120)

    # -----------------------------------------------------------
    # Core classify — single image, specific model
    # -----------------------------------------------------------

    def _classify_with_model(self, image_path, model):
        try:
            image = Image.open(image_path).convert("RGB")

            response = self.client.models.generate_content(
                model=model,
                contents=[
                    PROMPT,
                    image,
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ClassificationResult,
                ),
            )

            if response.parsed:
                return self._format_result(response.parsed)

            return self._error_result(
                "Gemini returned empty response"
            )

        except Exception as e:
            print("\n========== GEMINI ERROR ==========")
            print(f"Model: {model}")
            print(f"Image: {image_path}")
            print(type(e).__name__)
            print(str(e))
            print("==================================\n")

            raise

    # -----------------------------------------------------------
    # Single image classify (public)
    # -----------------------------------------------------------

    def classify(self, image_path):
        if USE_MOCK_GEMINI:
            return self._mock_result(image_path)

        models_to_try = [self.model]

        if self.fallback_model:
            models_to_try.append(self.fallback_model)

        for model in models_to_try:
            for attempt in range(6):
                try:
                    return self._classify_with_model(
                        image_path,
                        model,
                        # max_retries=1
                    )

                except genai_errors.APIError as e:

                    # Daily quota exhausted -> do NOT retry
                    if self._is_daily_quota_exceeded(e):
                        print(
                            f"Daily quota exhausted for {model}. "
                            f"Skipping this model."
                        )
                        break

                    code = getattr(e, "code", None)

                    # Retry only temporary errors
                    if code in RETRYABLE_CODES and attempt < 5:
                        wait = self._get_wait_time(
                            attempt,
                            e if code == 429 else None
                        )

                        print(
                            f"Temporary rate limit ({model}), "
                            f"retrying in {wait:.0f}s"
                        )

                        time.sleep(wait)
                        continue

                    break

                except Exception as e:
                    print(f"Unexpected error using {model}: {e}")
                    break

    # -----------------------------------------------------------
    # Rate-limited sequential
    # -----------------------------------------------------------

    def _rate_limited_classify(self, image_path):
        """
        Classify a single image with rate limiting and model fallback.

        The rate limiter ensures we stay within API quotas.
        Retries up to 5 times on retryable errors, switching models
        if quota is exhausted.
        """
        if not USE_MOCK_GEMINI:
            self.rate_limiter.wait()
            
        # self.rate_limiter.wait()

        models_to_try = [self.model]

        if self.fallback_model:
            models_to_try.append(self.fallback_model)

        for model in models_to_try:
            for attempt in range(6):
                try:
                    return self._classify_with_model(
                        image_path, model, 
                        # max_retries=1
                    )

                except genai_errors.APIError as e:
                    if self._is_daily_quota_exceeded(e):
                        print(
                            f"Daily quota exhausted. "
                            f"Stopping further API calls."
                        )
                        return self._error_result("daily quota exhausted")

                    code = getattr(e, "code", None)
                    if code in RETRYABLE_CODES and attempt < 5:
                        wait = self._get_wait_time(attempt, e if code == 429 else None)
                        label = "rate limited" if code == 429 else f"error {code}"
                        detail = f": {e}" if code == 429 else ""
                        print(f"  {label} ({model}), retrying in {wait:.0f}s{detail}")
                        time.sleep(wait)
                        continue
                    # This model failed permanently, try next
                    break
                except Exception as e:
                    print(f"\nUnexpected exception for {model}:")
                    print(type(e).__name__)
                    print(str(e))
                    raise

        print(
            f"  Model failed for {image_path.name}"
        )
        print(f"  Model: {self.model}")
        print(f"  API key exists: {bool(GEMINI_API_KEY)}")
        return self._error_result(
            f"failed after retries on all models"
        )

    # -----------------------------------------------------------
    # Public entry point for multiple images
    # -----------------------------------------------------------

    def classify_many(self, image_paths):
        """
        Classify multiple images sequentially with rate limiting.

        Each image is classified one at a time with pacing to
        stay within API rate limits. Individual failures are
        returned as error entries (category=None) so the pipeline
        can continue processing the remaining images.

        Returns a dict of {image_path: result_dict}.
        """
        paths = list(image_paths)
        if not paths:
            return {}

        results = {}
        
        if USE_MOCK_GEMINI:

            return {
                path: self._mock_result(path)
                for path in paths
            }

        for i, path in enumerate(paths):
            print(f"\r  [{i+1}/{len(paths)}] ", end="")

            try:
                result = self._rate_limited_classify(path)
                results[path] = result
                print(
                    f"{path.name}: {result['category']} "
                    f"({result['confidence']})"
                )
            except Exception as e:
                results[path] = self._error_result(f"error: {e}")
                print(f"{path.name}: FAILED ({e})")

        return results
    
    
    def _mock_result(self, image_path):
        h = hashlib.sha256(str(image_path).encode()).hexdigest()
        is_screenshot = int(h, 16) % 100 < 50

        if is_screenshot:

            return {
                "category": "screenshot",
                "confidence": 0.96,
                "source": "mock_gemini",
                "has_ui_elements": True,
                "orientation": "portrait",
                "scene_type": "phone_home_screen",
                "wallpaper_suitable": False,
                "wallpaper_reason":
                    "Contains UI elements.",
                "description":
                    "Mock screenshot result.",
                "prompt":
                    "Mock screenshot result.",
            }

        return {
            "category": "wallpaper",
            "confidence": 0.94,
            "source": "mock_gemini",
            "has_ui_elements": False,
            "orientation": "landscape",
            "scene_type": "photo",
            "wallpaper_suitable": True,
            "wallpaper_reason":
                "Suitable wallpaper image.",
            "description":
                "Mock wallpaper result.",
            "prompt":
                "Mock wallpaper result.",
        }


ai_classifier = AIClassifier()
