"""
UNUSED — Ollama-based local AI classifier.

Replaced by ai_classifier.py (Gemini API). Kept for reference.
"""

# import json
# import ollama
#
#
# PROMPT = """
# Classify the image as exactly one of:
#
# - screenshot
# - wallpaper
#
# Definitions:
#
# screenshot:
# - phone home screen
# - lock screen
# - app screen
# - browser screen
# - desktop screenshot
# - software interface
# - any visible UI elements
#
# wallpaper:
# - photograph
# - artwork
# - illustration
# - image without UI elements
#
# Return ONLY valid JSON.
#
# Example:
#
# {
#   "category": "screenshot",
#   "confidence": 0.95,
#   "reason": "contains app icons and status bar"
# }
# """
#
#
# class LocalAIClassifier:
#
#     def __init__(self):
#         self.model = "llava:7b"
#
#     def classify(self, image_path):
#
#         response = ollama.chat(
#             model=self.model,
#             messages=[
#                 {
#                     "role": "user",
#                     "content": PROMPT,
#                     "images": [str(image_path.resolve())]
#                 }
#             ]
#         )
#
#         print(f"Local AI response: {response}")
#
#         try:
#             result = json.loads(
#                 response["message"]["content"]
#             )
#
#             return {
#                 "category": result["category"],
#                 "confidence": round(
#                     float(result["confidence"]),
#                     3
#                 ),
#                 "source": "local_qwen",
#                 "prompt": result["reason"]
#             }
#
#         except Exception:
#
#             return {
#                 "category": None,
#                 "confidence": 0.0,
#                 "source": "local_qwen",
#                 "prompt": "failed to parse local response"
#             }
#
#
# local_ai_classifier = LocalAIClassifier()
