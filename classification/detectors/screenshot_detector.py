"""
Screenshot Detector

Determines how likely an image is a screenshot
(phone/tablet/desktop UI) using OpenCV features.
"""


class ScreenshotDetector:

    # Matches the threshold WallpaperDetector treats as
    # "no status bar" — keeps both detectors consistent so
    # they can't disagree on the same underlying signal.
    STATUS_BAR_THRESHOLD = 0.04

    def detect(self, f):

        score = 0

        # Status/navigation bar (clock, battery, wifi, nav icons).
        # NOTE: was `if f["top_density"]:` which is True for
        # almost any non-zero float — Canny finds *some* edge
        # in the top strip of nearly every image, including
        # plain wallpapers. That false positive was the main
        # reason almost everything scored as "screenshot".
        #
        # Device-agnostic bar check: phone/tablet screenshots put
        # the status bar at the TOP; laptop/desktop screenshots
        # usually put the clock/wifi/battery taskbar at the BOTTOM
        # (Windows) — occasionally at the top (macOS menu bar, some
        # Linux DEs). Checking both means we don't silently miss
        # desktop screenshots just because the bar isn't where a
        # phone would put it.
        has_top_bar = f["top_density"] > self.STATUS_BAR_THRESHOLD
        has_bottom_bar = f["bottom_density"] > self.STATUS_BAR_THRESHOLD

        if has_top_bar or has_bottom_bar:
            score += 1

        # Extra point if bars show up on BOTH edges — very characteristic
        # of a phone/tablet screenshot (status bar + nav bar together),
        # but not required, so laptop screenshots with only one bar
        # still get credit for the base signal above.
        if has_top_bar and has_bottom_bar:
            score += 1

        # Home screen icons
        if f["icon_count"] >= 12:
            score += 2

        # Widgets
        if f["widget_count"] >= 1:
            score += 2

        # App grid
        if f["grid_score"] > 0.30:
            score += 2

        # Text labels
        if f["text_regions"] >= 8:
            score += 1

        max_score = 9  # was 8; +1 for the new top+bottom bonus point

        confidence = score / max_score

        return {
            "candidate": score >= 5,
            "confidence": round(confidence, 2),
        }


screenshot_detector = ScreenshotDetector()