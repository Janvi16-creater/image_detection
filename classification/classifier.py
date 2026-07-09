"""
UNUSED — ImageClassifier wrapper around Gemini.

The pipeline now uses hybrid_classifier.py directly.
Kept for reference.
"""

# from classification.ai_classifier import ai_classifier
#
#
# class ImageClassifier:
#
#     def classify(self, image_path, image=None):
#
#         # `image` (the cv2-loaded array) isn't needed here anymore —
#         # Gemini reads the file directly. It's kept as an accepted
#         # argument so image_pipeline.py doesn't need to change its
#         # call signature.
#
#         result = ai_classifier.classify(image_path)
#
#         print(f"{image_path.name}: {result['category']} "
#               f"({result['confidence']}) — {result['prompt']}")
#
#         return result
#
#
# image_classifier = ImageClassifier()
