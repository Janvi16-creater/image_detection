"""
Image Validation
"""

from PIL import Image


def validate_image(image_path):
    """
    Validate whether an image is readable.

    Returns
    -------
    tuple
        (bool, reason)
    """

    try:

        with Image.open(image_path) as img:

            img.verify()

        return True, "Valid"

    except Exception as e:

        return False, str(e)