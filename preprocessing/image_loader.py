"""
Image Loader

Loads images one by one using a generator.
"""

from pathlib import Path

from config import SUPPORTED_EXTENSIONS


def load_images(dataset_path):
    """
    Yield image paths one at a time.

    Parameters
    ----------
    dataset_path : str | Path

    Yields
    ------
    Path
    """

    dataset_path = Path(dataset_path)

    if not dataset_path.exists():
        raise FileNotFoundError(f"{dataset_path} does not exist.")

    for image in dataset_path.rglob("*"):

        if image.is_file() and image.suffix.lower() in SUPPORTED_EXTENSIONS:

            yield image