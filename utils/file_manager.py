"""
Move Files
"""

import shutil
from pathlib import Path


def move_file(src, destination):

    destination.mkdir(parents=True, exist_ok=True)

    shutil.copy2(str(src), str(destination / Path(src).name))