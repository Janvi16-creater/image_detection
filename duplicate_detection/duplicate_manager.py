"""
Duplicate Manager
"""

from duplicate_detection.sha256_duplicate import sha256_hash
from duplicate_detection.phash_duplicate import perceptual_hash


class DuplicateManager:

    def __init__(self, threshold=8):

        self.sha_hashes = {}

        self.phashes = {}

        self.threshold = threshold

    def is_duplicate(self, image_path):

        sha = sha256_hash(image_path)

        if sha in self.sha_hashes:

            return True, "Exact Duplicate"

        self.sha_hashes[sha] = image_path

        phash = perceptual_hash(image_path)

        for old_hash in self.phashes:

            if phash - old_hash <= self.threshold:

                return True, "Near Duplicate"

        self.phashes[phash] = image_path

        return False, "Unique"
    
duplicate_manager = DuplicateManager()