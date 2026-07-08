"""
Project Configuration
"""

from pathlib import Path
import torch

# -------------------------------------------------
# Project Root
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

# -------------------------------------------------
# Dataset
# -------------------------------------------------

DATASET_DIR = PROJECT_ROOT / "dataset"
RAW_DATASET = DATASET_DIR / "raw"

# -------------------------------------------------
# Output
# -------------------------------------------------

OUTPUT_DIR = PROJECT_ROOT / "output"


CORRUPTED_DIR = OUTPUT_DIR / "corrupted"
DUPLICATE_DIR = OUTPUT_DIR / "duplicates"

SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
WALLPAPER_DIR = OUTPUT_DIR / "wallpapers"


BLUR_DIR = OUTPUT_DIR / "blurry"
LOW_RESOLUTION_DIR = OUTPUT_DIR / "low_resolution"
UNKNOWN_DIR = OUTPUT_DIR / "unknown"
REPORT_DIR = OUTPUT_DIR / "reports"

SUPPORTED_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
    ".tif",
    ".tiff"
)
