"""
Perceptual Hash
"""

import imagehash
from PIL import Image


def perceptual_hash(image_path):

    with Image.open(image_path) as img:

        return imagehash.phash(img)