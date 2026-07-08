"""
AI Classifier using SigLIP

Only called when OpenCV confidence is low.
"""

import torch
from PIL import Image

from classification.model_loader import vision_model


LABELS = [

    "mobile phone screenshot with status bar and app interface",

    "computer screenshot with browser window and user interface",

    "desktop screenshot showing software or application",

    "phone lock screen screenshot",

    "digital wallpaper or background image",

    "photograph captured using a camera",

    "nature wallpaper",

    "anime wallpaper",

    "abstract wallpaper",

    "illustration artwork"

]


class AIClassifier:

    def classify(self, image_path):

        image = Image.open(image_path).convert("RGB")

        inputs = vision_model.processor(

            images=image,

            text=LABELS,

            return_tensors="pt",

            padding=True

        )

        with torch.no_grad():

            outputs = vision_model.model(**inputs)

        probs = outputs.logits_per_image.softmax(dim=-1)[0]

        index = torch.argmax(probs).item()

        confidence = float(probs[index])

        label = LABELS[index].lower()

        # ---------------------------------------
        # Convert prompt to category
        # ---------------------------------------

        screenshot_words = [

            "screenshot",

            "interface",

            "browser",

            "software",

            "lock screen",

            "status bar",

            "app"

        ]

        if any(word in label for word in screenshot_words):

            category = "screenshot"

        else:

            category = "wallpaper"

        return {

            "category": category,

            "confidence": round(confidence, 3),

            "source": "siglip",

            "prompt": LABELS[index]

        }


ai_classifier = AIClassifier()