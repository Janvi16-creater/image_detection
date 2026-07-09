"""
UNUSED — SigLIP vision model loader.

Kept for reference; was intended for local VLM classification
but the project uses Gemini API instead.
"""

# from transformers import (
#     AutoProcessor,
#     AutoModelForZeroShotImageClassification,
# )
#
# MODEL_NAME = "google/siglip-base-patch16-224"
#
#
# class VisionModel:
#
#     def __init__(self):
#
#         print("Loading SigLIP...")
#
#         self.processor = AutoProcessor.from_pretrained(MODEL_NAME)
#
#         self.model = AutoModelForZeroShotImageClassification.from_pretrained(
#             MODEL_NAME
#         )
#
#         self.model.eval()
#
#
# vision_model = VisionModel()
