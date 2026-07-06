"""
Exception Handler
"""

import traceback


class ExceptionHandler:

    @staticmethod
    def handle(image_path, exception):

        print("\n-------------------------------------")
        print("Processing Failed")
        print("-------------------------------------")
        print(f"Image : {image_path}")
        print(f"Error : {exception}")
        print(traceback.format_exc())
        print("-------------------------------------\n")