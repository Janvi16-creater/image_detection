"""
Main Pipeline
"""

from config import *
from preprocessing.image_loader import load_images
from preprocessing.validator import validate_image
from duplicate_detection.duplicate_manager import DuplicateManager
from utils.file_manager import move_file
from utils.logger import get_logger


logger = get_logger()


def create_output_dirs():

    for folder in OUTPUT_FOLDERS:

        folder.mkdir(parents=True, exist_ok=True)


def main():

    create_output_dirs()

    duplicate_manager = DuplicateManager()

    for image in load_images(RAW_DATASET):

        logger.info(f"Processing {image.name}")

        valid, reason = validate_image(image)

        if not valid:

            logger.warning(reason)

            move_file(image, CORRUPTED_DIR)

            continue

        duplicate, reason = duplicate_manager.is_duplicate(image)

        if duplicate:

            logger.info(reason)

            move_file(image, DUPLICATE_DIR)

            continue

        logger.info("Image Passed Phase 1")

        move_file(image, CLEAN_DIR)


if __name__ == "__main__":

    main()