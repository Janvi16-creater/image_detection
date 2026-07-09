"""
UNUSED — Standalone Ollama debug script.

Not part of the pipeline. Kept for reference.
"""

# from PIL import Image
# import requests
# import base64
#
# print("Creating image...")
#
# img = Image.new("RGB", (512, 512), color=(255, 0, 0))
# img.save("test_simple.jpg")
#
# print("Image created.")
#
# print("Reading image...")
#
# with open("test_simple.jpg", "rb") as f:
#     image_data = base64.b64encode(
#         f.read()
#     ).decode()
#
# print("Image encoded.")
#
# print("Sending request to Ollama...")
#
# response = requests.post(
#     "http://localhost:11434/api/chat",
#     json={
#         "model": "llava:7b",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "Describe this image.",
#                 "images": [image_data]
#             }
#         ],
#         "stream": False
#     },
#     timeout=300
# )
#
# print("Response received.")
#
# print(response.status_code)
# print(response.text)

from google import genai
from config import GEMINI_API_KEY

from PIL import Image

client = genai.Client(api_key=GEMINI_API_KEY)

img = Image.open(r"D:\image_detection\dataset\raw\img (1).webp")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        "Is this a screenshot or wallpaper?",
        img
    ]
)

print(response.text)