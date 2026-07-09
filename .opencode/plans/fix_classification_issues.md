# Fix Classification Issues - Implementation Plan

## Problem

4 images (5, 9, 13, 15) are misclassified as "screenshot" when they are actually wallpapers.
- All have 0 icons, 0 widgets, 0 grid score
- All have high text_regions (68-121) from image texture, not real text
- ss_score=0.45, wp_score=0.35 (both low, close)
- Tiebreaker forces "screenshot" when Gemini is unavailable

## Fix 1: `classification/hybrid_classifier.py` — `_force_opencv_decision()`

**Current (lines 39-44):**
```python
if abs(ss - wp) < 0.10:
    cv_result["category"] = "screenshot"
elif ss >= wp:
    cv_result["category"] = "screenshot"
else:
    cv_result["category"] = "wallpaper"
```

**Change to:**
```python
if abs(ss - wp) < 0.10 and max(ss, wp) < 0.5:
    cv_result["category"] = "wallpaper"
elif ss >= wp:
    cv_result["category"] = "screenshot"
else:
    cv_result["category"] = "wallpaper"
```

When both detectors are uncertain (< 0.5) and scores are close, prefer wallpaper — images with no real UI icons/widgets/grid are more likely detail-rich wallpapers.

## Fix 2: `classification/detectors/screenshot_detector.py` — text scoring

**Current (lines 61-66):** Text regions always add up to +3 points regardless of whether there are any actual UI elements.

**Change to:** Only count text regions toward screenshot score when there's at least some real UI evidence (icons, widgets, or grid):

```python
# Text labels only count if there's real UI evidence
has_ui_evidence = f["icon_count"] > 0 or f["widget_count"] > 0 or f["grid_score"] > 0.2
if has_ui_evidence or f["text_regions"] >= 8:
    if f["text_regions"] >= 8:
        score += 1
    if f["text_regions"] >= 20:
        score += 1
    if f["text_regions"] >= 40:
        score += 1
```

This prevents texture-rich wallpapers from scoring screenshot points for false text detection.

## Fix 3: `classification/hybrid_classifier.py` — `_enrich_cv_result()`

**Current:** derives scene_type, has_ui, wallpaper_suitable from raw features independently of final category.

**Change to:** align enrichment with the final category:

```python
if category == "screenshot":
    has_ui = True
    scene_type = "phone_home_screen" if grid_score > 0.3 else "app_screen"
    wallpaper_suitable = False
    wallpaper_reason = "Contains UI elements"
else:
    has_ui = False
    scene_type = "photo" if edge_density > 0.08 else "abstract"
    wallpaper_suitable = wp_score >= 0.5
    wallpaper_reason from reasons list
```

## Expected Results After All 3 Fixes

| Image | Current | After |
|-------|---------|-------|
| img (5).webp | screenshot, app_screen | **wallpaper**, photo |
| img (9).webp | screenshot, app_screen | **wallpaper**, photo |
| img (13).webp | screenshot, app_screen | **wallpaper**, photo |
| img (15).webp | screenshot, app_screen | **wallpaper**, photo |
| img (6)-(8).webp | screenshot, phone_home_screen | screenshot, phone_home_screen (unchanged — they have real icons) |
| img (2).webp | wallpaper, app_screen | **wallpaper, photo** (scene_type fixed) |

## Testing

1. Set `USE_MOCK_GEMINI = True` in `ai_classifier.py`
2. Run `python main.py`
3. Verify images 5, 9, 13, 15 are now classified as "wallpaper"
4. Verify enrichment fields (scene_type, wallpaper_suitable) are consistent
5. Set `USE_MOCK_GEMINI = False` after testing
