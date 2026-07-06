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

            # -----------------------------
            # Phase 1
            # -----------------------------

            "clean":
                self.output_dir / "clean",

            "duplicates":
                self.output_dir / "duplicates",

            "corrupted":
                self.output_dir / "corrupted",

            # -----------------------------
            # Phase 2
            # -----------------------------

            "screenshots":
                self.output_dir / "screenshots",

            "wallpapers":
                self.output_dir / "wallpapers",

            "widgets":
                self.output_dir / "widgets",

            "documents":
                self.output_dir / "documents",

            "camera_photos":
                self.output_dir / "camera_photos",

            "unknown":
                self.output_dir / "unknown",

            # -----------------------------
            # Phase 3
            # -----------------------------

            "blurry":
                self.output_dir / "blurry",

            "noisy":
                self.output_dir / "noisy",

            "overexposed":
                self.output_dir / "overexposed",

            "underexposed":
                self.output_dir / "underexposed",

            "low_resolution":
                self.output_dir / "low_resolution"

        }

    # --------------------------------------------------------

    def create_folders(self):

        """
        Create every folder if it
        does not already exist.
        """

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        for folder in self.folders.values():

            folder.mkdir(
                parents=True,
                exist_ok=True
            )

    # --------------------------------------------------------

    def get_folder(self, category):

        """
        Return folder path.
        """

        mapping = {
            "screenshot": "screenshots",
            "wallpaper": "wallpapers",
            "widget": "widgets",
            "document": "documents",
            "camera_photo": "camera_photos",
            "camera photograph": "camera_photos",
            "camera_photos": "camera_photos",
            "mobile screenshot": "screenshots",
            "desktop screenshot": "screenshots",
            "application widget": "widgets",
        }

        mapped_category = mapping.get(category, category)

        return self.folders.get(
            mapped_category,
            self.folders["unknown"]
        )

    # --------------------------------------------------------

    def list_folders(self):

        """
        Return dictionary of folders.
        """

        return self.folders


folder_manager = FolderManager()