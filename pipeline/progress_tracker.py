"""
Progress Tracker
"""

import time


class ProgressTracker:

    def __init__(self, total):

        self.total = total
        self.current = 0
        self.start = time.time()

    def update(self):

        self.current += 1

        percentage = self.current / self.total * 100

        print(
            f"\rProcessing {self.current}/{self.total}"
            f" ({percentage:.2f}%)",
            end=""
        )

    def finish(self):

        elapsed = time.time() - self.start

        print(f"\nCompleted in {elapsed:.2f} seconds.")