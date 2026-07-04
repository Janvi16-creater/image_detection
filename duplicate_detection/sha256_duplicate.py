"""
SHA256 Duplicate Detection
"""

import hashlib


def sha256_hash(image_path):
    """
    Compute SHA256 hash.
    """

    sha = hashlib.sha256()

    with open(image_path, "rb") as f:

        while True:

            chunk = f.read(8192)

            if not chunk:
                break

            sha.update(chunk)

    return sha.hexdigest()