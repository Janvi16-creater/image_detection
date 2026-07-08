"""
Main Entry Point

Workflow:

1. Create output folders
2. Load dataset
3. Run image processing pipeline
4. Generate reports
"""

from cv2 import error
import traceback
from config import (
    RAW_DATASET,
    OUTPUT_DIR,
)

from pipeline.image_pipeline import ImagePipeline


# def create_output_directories():
#     """
#     Create all required output directories.
#     """

#     for folder in OUTPUT_DIR:
#         folder.mkdir(
#             parents=True,
#             exist_ok=True,
#         )


def main():

    print("=" * 60)
    print("        IMAGE DATASET CLEANING PIPELINE")
    print("=" * 60)

    # create_output_directories()

    if not RAW_DATASET.exists():

        print(f"\nDataset not found:\n{RAW_DATASET}")

        return

    pipeline = ImagePipeline(
        dataset_path=RAW_DATASET
    )

    pipeline.run()

    print("\n")
    print("=" * 60)
    print("Pipeline Completed Successfully.")
    print("=" * 60)


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\nPipeline Interrupted by User.")


    except Exception as error:

        print(error)
        traceback.print_exc()