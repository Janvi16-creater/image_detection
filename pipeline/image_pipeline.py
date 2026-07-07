"""
Main Image Pipeline
"""

import shutil
import cv2

from config import OUTPUT_DIR
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
        
        if OUTPUT_DIR.exists():

            shutil.rmtree(OUTPUT_DIR)

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

                        file_manager.copy_file(
                            image_path,
                            destination
                        )
                        
                        logger.log(

                            filename=image_path.name,

                            category="corrupted",

                            confidence=1.0,

                            source="validator",

                            blur="-",

                            noise="-",

                            exposure="-",

                            resolution="-",

                            status="Corrupted"

                        )
                        
                        report_generator.add_record(

                            filename=image_path.name,

                            category="corrupted",

                            confidence=1.0,

                            source="validator",

                            blur="-",

                            noise="-",

                            exposure="-",

                            resolution="-",

                            status="Corrupted"
                        )
                    

                        continue

                    # -----------------------------
                    # Duplicate Detection
                    # -----------------------------

                    is_duplicate, duplicate_reason = duplicate_manager.is_duplicate(image_path)
                    print(
                        image_path.name,
                        "Duplicate:",
                        is_duplicate,
                        duplicate_reason
                    )
                    if is_duplicate:

                        destination = folder_manager.get_folder(
                            "duplicates"
                        )
                        
                        print("COPYING DUPLICATE TO:", destination)

                        file_manager.copy_file(
                            image_path,
                            destination
                        )
                        
                        logger.log(

                            filename=image_path.name,

                            category="duplicate",

                            confidence=1.0,

                            source="duplicate_detector",

                            blur="-",

                            noise="-",

                            exposure="-",

                            resolution="-",

                            status="Duplicate"

                        )
                        
                        report_generator.add_record(

                            filename=image_path.name,

                            category="duplicate",

                            confidence=1.0,

                            source="duplicate_detector",

                            blur="-",

                            noise="-",

                            exposure="-",

                            resolution="-",

                            status="Duplicate"

                    )

                        continue
                    
                    # -----------------------------
                    # Load Image (Only Once)
                    # -----------------------------

                    image = cv2.imread(str(image_path))

                    if image is None:
                        raise ValueError(f"Unable to read image: {image_path}")

                    # -----------------------------
                    # Classification
                    # -----------------------------

                    classification = image_classifier.classify(
                        image_path,
                        image
                    )

                    category = classification["category"]

                    confidence = classification["confidence"]

                    # -----------------------------
                    # Quality
                    # -----------------------------

                    blur = blur_detector.detect(image)

                    noise = noise_detector.detect(image)

                    exposure = exposure_detector.detect(image)

                    resolution = resolution_detector.detect(image)

                    # -----------------------------
                    # Accept / Reject
                    # -----------------------------

                    # status = "Accepted"

                    # destination = folder_manager.get_folder(category)

                    # if blur["is_blurry"]:

                    #     destination = folder_manager.get_folder(
                    #         "blurry"
                    #     )

                    #     status = "Rejected"

                    # elif noise["is_noisy"]:

                    #     destination = folder_manager.get_folder(
                    #         "noisy"
                    #     )

                    #     status = "Rejected"

                    # elif not exposure["is_good_exposure"]:

                    #     if exposure["label"] == "overexposed":

                    #         destination = folder_manager.get_folder(
                    #             "overexposed"
                    #         )

                    #     else:

                    #         destination = folder_manager.get_folder(
                    #             "underexposed"
                    #         )

                    #     status = "Rejected"

                    # elif not resolution["is_good_resolution"]:

                    #     destination = folder_manager.get_folder(
                    #         "low_resolution"
                    #     )

                    #     status = "Rejected"
                    
                    # -----------------------------
                    # Quality Decision
                    # -----------------------------

                    status = "Accepted"
                    quality = "accepted"

                    # Blur

                    if blur["is_blurry"]:

                        quality = "blurry"
                        status = "Rejected"

                    # Noise

                    elif noise["is_noisy"]:

                        quality = "noisy"
                        status = "Rejected"

                    # Exposure

                    elif not exposure["is_good_exposure"]:

                        status = "Rejected"

                        if exposure["label"] == "overexposed":

                            quality = "overexposed"

                        else:

                            quality = "underexposed"

                    # Resolution

                    elif not resolution["is_good_resolution"]:

                        quality = "low_resolution"
                        status = "Rejected"

                    # -----------------------------
                    # Final Destination
                    # -----------------------------

                    destination = folder_manager.get_folder(
                        category,
                        quality
                    )

                    # -----------------------------
                    # Move File
                    # -----------------------------

                    file_manager.copy_file(
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
                        
                        source = classification["source"],

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
                        
                        source = classification["source"],

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