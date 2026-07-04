"""File and directory utility helpers."""
from pathlib import Path


def create_directories(*directories):
    """
    Create directories if they do not exist.
    """
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)