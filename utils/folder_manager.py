"""
Folder Manager

Responsible for:
- Creating output folders
- Checking folder existence
- Returning folder paths
"""

from pathlib import Path


def create_directories(*directories):
    """
    Create directories if they do not exist.
    """
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


class FolderManager:

    def __init__(self, output_dir="output"):

        self.output_dir = Path(output_dir)

        self.folders = {

        "clean": self.output_dir / "clean",

        "duplicates": self.output_dir / "duplicates",

        "corrupted": self.output_dir / "corrupted",

        "screenshots": self.output_dir / "screenshots",

        "wallpapers": self.output_dir / "wallpapers",

        "widgets": self.output_dir / "widgets",

        "documents": self.output_dir / "documents",

        "original": self.output_dir / "original",

        "reports": self.output_dir / "reports",

    }

    # --------------------------------------------------------

    def create_folders(self):

        qualities = [

            "accepted",
            "blurry",
            "noisy",
            "underexposed",
            "overexposed",
            "low_resolution"

        ]

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # Category folders
        categories = [
            "wallpapers",
            "widgets",
            "screenshots",
            "documents",
            "original"
        ]

        for category in categories:

            base = self.output_dir / category

            base.mkdir(
                parents=True,
                exist_ok=True
            )

            for quality in qualities:

                (base / quality).mkdir(
                    parents=True,
                    exist_ok=True
                )

        # Special folders
        (self.output_dir / "duplicates").mkdir(exist_ok=True)
        (self.output_dir / "corrupted").mkdir(exist_ok=True)
        (self.output_dir / "reports").mkdir(exist_ok=True)

    # --------------------------------------------------------

    def get_folder(self, category, quality="accepted"):
        """
        Returns output folder based on category and quality.

        Example:
            widgets/accepted
            widgets/blurry
        """

        mapping = {

            "wallpaper": "wallpapers",
            "wallpapers": "wallpapers",

            "screenshot": "screenshots",
            "screenshots": "screenshots",

            "widget": "widgets",
            "widgets": "widgets",

            "document": "documents",
            "documents": "documents",

            "original": "original",
            "unknown": "original",
            
            "duplicate": "duplicates",
            "duplicates": "duplicates",
            "corrupted": "corrupted",

        }

        category_folder = mapping.get(category, "original")

        destination = self.output_dir / category_folder / quality

        destination.mkdir(
            parents=True,
            exist_ok=True
        )

        return destination

    # --------------------------------------------------------

    def list_folders(self):
        """
        Return dictionary of folders.
        """

        return self.folders


folder_manager = FolderManager()
