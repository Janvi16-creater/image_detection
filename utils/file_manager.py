"""
File Manager

Responsible for:

- Moving images
- Copying images
- Renaming duplicate filenames
"""

import shutil
from pathlib import Path


class FileManager:

    def __init__(self):
        pass

    # --------------------------------------------------

    def move_file(self, source, destination_folder):

        source = Path(source)
        destination_folder = Path(destination_folder)

        destination_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        destination = destination_folder / source.name

        counter = 1

        while destination.exists():

            destination = (
                destination_folder
                / f"{source.stem}_{counter}{source.suffix}"
            )

            counter += 1

        shutil.copy2(
            str(source),
            str(destination)
        )

        return destination

    # --------------------------------------------------

    def copy_file(self, source, destination_folder):

        source = Path(source)
        destination_folder = Path(destination_folder)

        destination_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        destination = destination_folder / source.name

        shutil.copy2(
            str(source),
            str(destination)
        )

        return destination

    # --------------------------------------------------

    def delete_file(self, file_path):

        file_path = Path(file_path)

        if file_path.exists():

            file_path.unlink()

            return True

        return False

    # --------------------------------------------------

    def file_exists(self, file_path):

        return Path(file_path).exists()


file_manager = FileManager()