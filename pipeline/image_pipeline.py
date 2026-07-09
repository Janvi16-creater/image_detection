"""
Main Image Pipeline
"""

import shutil
import cv2

from config import OUTPUT_DIR

from preprocessing.image_loader import load_images
from preprocessing.validator import validate_image

from duplicate_detection.duplicate_manager import duplicate_manager
from classification.hybrid_classifier import hybrid_classifier

from quality.blur_detector import blur_detector
from quality.noise_detector import noise_detector
from quality.exposure_detector import exposure_detector
from quality.resolution_detector import resolution_detector

from utils.folder_manager import folder_manager
from utils.file_manager import file_manager
from utils.logger import logger

from reports.report_generator import report_generator

from pipeline.progress_tracker import ProgressTracker
from pipeline.batch_processor import batch_generator
from pipeline.exception_handler import ExceptionHandler


class ImagePipeline:

    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

    # ---------------------------------------------------------

    def _log_and_report(self, **kwargs):
        logger.log(**kwargs)
        report_generator.add_record(**kwargs)

    # ---------------------------------------------------------

    def run(self):

        if OUTPUT_DIR.exists():
            shutil.rmtree(OUTPUT_DIR)

        folder_manager.create_folders()

        images = list(load_images(self.dataset_path))

        progress = ProgressTracker(len(images))

        all_classification_candidates = []
        batch_classifications = {}

        for batch in batch_generator(images, batch_size=10):

            # -------------------------------------------------
            # Pass 1 — Validation + Duplicate Detection
            # -------------------------------------------------

            classification_candidates = []

            for image_path in batch:

                try:
                    progress.update()

                    valid, _ = validate_image(image_path)

                    if not valid:
                        destination = folder_manager.get_folder("corrupted")
                        file_manager.copy_file(image_path, destination)

                        self._log_and_report(
                            filename=image_path.name,
                            category="corrupted",
                            confidence=1.0,
                            source="validator",
                            blur="-", noise="-", exposure="-",
                            resolution="-",
                            status="Corrupted",
                        )
                        continue

                    duplicate, _ = duplicate_manager.is_duplicate(image_path)

                    if duplicate:
                        destination = folder_manager.get_folder("duplicates")
                        file_manager.copy_file(image_path, destination)

                        self._log_and_report(
                            filename=image_path.name,
                            category="duplicate",
                            confidence=1.0,
                            source="duplicate_detector",
                            blur="-", noise="-", exposure="-",
                            resolution="-",
                            status="Duplicate",
                        )
                        continue

                    classification_candidates.append(image_path)

                except Exception as exception:
                    ExceptionHandler.handle(image_path, exception)

            # -------------------------------------------------
            # Pass 2 — Classification (batch via hybrid)
            # -------------------------------------------------

            if classification_candidates:
                batch_results = hybrid_classifier.classify_many(
                    classification_candidates
                )
                batch_classifications.update(batch_results)

            all_classification_candidates.extend(classification_candidates)

        # -------------------------------------------------
        # Pass 3 — Quality checks + logging
        # -------------------------------------------------

        progress = ProgressTracker(len(all_classification_candidates))

        for image_path in all_classification_candidates:

            try:
                progress.update()

                classification = batch_classifications.get(image_path)

                if classification is None:
                    destination = folder_manager.get_folder("unknown")
                    file_manager.copy_file(image_path, destination)
                    self._log_and_report(
                        filename=image_path.name,
                        category="unknown",
                        confidence=0.0,
                        source="none",
                        blur="-", noise="-", exposure="-",
                        resolution="-",
                        status="Rejected",
                        description="no classification result",
                    )
                    continue

                if classification["category"] is None:
                    destination = folder_manager.get_folder("unknown")
                    file_manager.copy_file(image_path, destination)
                    self._log_and_report(
                        filename=image_path.name,
                        category="unknown",
                        confidence=classification.get("confidence", 0.0),
                        source=classification.get("source", "unknown"),
                        blur="-", noise="-", exposure="-",
                        resolution="-",
                        status="Rejected",
                        description=classification.get(
                            "prompt",
                            classification.get("wallpaper_reason", "-"),
                        ),
                    )
                    continue

                category = classification["category"]
                confidence = classification.get("confidence", 0.0)
                source = classification.get("source", "unknown")

                image = cv2.imread(str(image_path))

                if image is None:
                    raise ValueError(
                        f"Unable to read image: {image_path}"
                    )

                blur = blur_detector.detect(image)
                noise = noise_detector.detect(image)
                exposure = exposure_detector.detect(image)
                resolution = resolution_detector.detect(image)

                status = "Accepted"
                quality = "accepted"

                if blur["is_blurry"]:
                    quality = "blurry"
                    status = "Rejected"
                elif noise["is_noisy"]:
                    quality = "noisy"
                    status = "Rejected"
                elif not exposure["is_good_exposure"]:
                    status = "Rejected"
                    quality = exposure["label"]
                elif not resolution["is_good_resolution"]:
                    quality = "low_resolution"
                    status = "Rejected"

                destination = folder_manager.get_folder(category, quality)
                file_manager.copy_file(image_path, destination)

                self._log_and_report(
                    filename=image_path.name,
                    category=category,
                    confidence=confidence,
                    source=source,
                    blur=blur["label"],
                    noise=noise["label"],
                    exposure=exposure["label"],
                    resolution=resolution["resolution_label"],
                    status=status,
                    orientation=classification.get("orientation", "-"),
                    scene_type=classification.get("scene_type", "-"),
                    has_ui_elements=classification.get("has_ui_elements", "-"),
                    wallpaper_suitable=classification.get("wallpaper_suitable", "-"),
                    description=classification.get(
                        "description",
                        classification.get("prompt", "-"),
                    ),
                    wallpaper_reason=classification.get("wallpaper_reason", "-"),
                )

            except Exception as exception:
                ExceptionHandler.handle(image_path, exception)

        progress.finish()
        report_generator.save()


# UNUSED
# image_pipeline = ImagePipeline
