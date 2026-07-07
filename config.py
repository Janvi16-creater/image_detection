"""
Project Configuration
"""

from pathlib import Path

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

CLEAN_DIR = OUTPUT_DIR / "clean"
CORRUPTED_DIR = OUTPUT_DIR / "corrupted"
DUPLICATE_DIR = OUTPUT_DIR / "duplicates"

SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"
WALLPAPER_DIR = OUTPUT_DIR / "wallpapers"
WIDGET_DIR = OUTPUT_DIR / "widgets"
DOCUMENT_DIR = OUTPUT_DIR / "documents"

BLUR_DIR = OUTPUT_DIR / "blurry"
LOW_RESOLUTION_DIR = OUTPUT_DIR / "low_resolution"
UNKNOWN_DIR = OUTPUT_DIR / "unknown"
REPORT_DIR = OUTPUT_DIR / "reports"

# -------------------------------------------------
# Supported Extensions
# -------------------------------------------------

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".webp",
    ".tiff",
}

# -------------------------------------------------
# Thresholds
# -------------------------------------------------

PHASH_THRESHOLD = 8

BLUR_THRESHOLD = 100

LOW_RESOLUTION_WIDTH = 720
LOW_RESOLUTION_HEIGHT = 720

# -------------------------------------------------
# AI Model
# -------------------------------------------------

MODEL_NAME = "google/siglip-base-patch16-224"

# -------------------------------------------------
# Create Output Directories
# -------------------------------------------------

OUTPUT_FOLDERS = [
    CLEAN_DIR,
    CORRUPTED_DIR,
    DUPLICATE_DIR,
    SCREENSHOT_DIR,
    WALLPAPER_DIR,
    WIDGET_DIR,
    DOCUMENT_DIR,
    BLUR_DIR,
    LOW_RESOLUTION_DIR,
    UNKNOWN_DIR,
    REPORT_DIR,
]

MODEL_NAME = "google/siglip-base-patch16-224"