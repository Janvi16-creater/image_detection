"""
Main Image Pipeline
"""

from preprocessing.image_loader import load_images
from preprocessing.validator import validate_image

from duplicate_detection.duplicate_manager import duplicate_manager

from classification.classifier import image_classifier

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

    def run(self):

        folder_manager.create_folders()

        images = list(load_images(self.dataset_path))

        progress = ProgressTracker(len(images))

        for batch in batch_generator(images, batch_size=100):

            for image_path in batch:

                try:

                    progress.update()

                    # -----------------------------
                    # Validation
                    # -----------------------------

                    is_valid, validation_reason = validate_image(image_path)
                    if not is_valid:

                        destination = folder_manager.get_folder(
                            "corrupted"
                        )

                        file_manager.move_file(
                            image_path,
                            destination
                        )

                        continue

                    # -----------------------------
                    # Duplicate Detection
                    # -----------------------------

                    is_duplicate, duplicate_reason = duplicate_manager.is_duplicate(image_path)
                    if is_duplicate:

                        destination = folder_manager.get_folder(
                            "duplicates"
                        )

                        file_manager.move_file(
                            image_path,
                            destination
                        )

                        continue

                    # -----------------------------
                    # Classification
                    # -----------------------------

                    classification = image_classifier.classify(
                        image_path
                    )

                    category = classification["category"]

                    confidence = classification["confidence"]

                    # -----------------------------
                    # Quality
                    # -----------------------------

                    blur = blur_detector.detect(image_path)

                    noise = noise_detector.detect(image_path)

                    exposure = exposure_detector.detect(image_path)

                    resolution = resolution_detector.detect(image_path)

                    # -----------------------------
                    # Accept / Reject
                    # -----------------------------

                    status = "Accepted"

                    destination = folder_manager.get_folder(category)

                    if blur["is_blurry"]:

                        destination = folder_manager.get_folder(
                            "blurry"
                        )

                        status = "Rejected"

                    elif noise["is_noisy"]:

                        destination = folder_manager.get_folder(
                            "noisy"
                        )

                        status = "Rejected"

                    elif not exposure["is_good_exposure"]:

                        if exposure["label"] == "overexposed":

                            destination = folder_manager.get_folder(
                                "overexposed"
                            )

                        else:

                            destination = folder_manager.get_folder(
                                "underexposed"
                            )

                        status = "Rejected"

                    elif not resolution["is_good_resolution"]:

                        destination = folder_manager.get_folder(
                            "low_resolution"
                        )

                        status = "Rejected"

                    # -----------------------------
                    # Move File
                    # -----------------------------

                    file_manager.move_file(
                        image_path,
                        destination
                    )

                    # -----------------------------
                    # Log
                    # -----------------------------

                    logger.log(

                        filename=image_path.name,

                        category=category,

                        confidence=confidence,

                        blur=blur["label"],

                        noise=noise["label"],

                        exposure=exposure["label"],

                        resolution=resolution[
                            "resolution_label"
                        ],

                        status=status

                    )

                    # -----------------------------
                    # Report
                    # -----------------------------

                    report_generator.add_record(

                        filename=image_path.name,

                        category=category,

                        confidence=confidence,

                        blur=blur["label"],

                        noise=noise["label"],

                        exposure=exposure["label"],

                        resolution=resolution[
                            "resolution_label"
                        ],

                        status=status

                    )

                except Exception as exception:

                    ExceptionHandler.handle(
                        image_path,
                        exception
                    )

        progress.finish()

        report_generator.save()