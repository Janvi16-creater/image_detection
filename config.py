"""
Project Configuration
"""

import os
 
from pathlib import Path
 
from dotenv import load_dotenv
 
 
# -------------------------------------------------
# Environment / API Keys
# -------------------------------------------------
# Loads variables from a .env file in the project root into the
# process environment. This must run before we read any of them
# with os.getenv() below.
 
load_dotenv()
 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
 
if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Create a .env file in the project "
        "root (next to this config.py) containing:\n"
        "    GEMINI_API_KEY=your-api-key-here"
    )

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
