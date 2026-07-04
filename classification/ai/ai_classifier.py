"""
AI Classifier using CLIP (Zero-Shot)

This module loads the CLIP model once and predicts
the probability that an image belongs to one of the
supported categories.
"""

from pathlib import Path

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


class AIClassifier:
    """
    Singleton AI classifier.

    The model is loaded only once.
    """

    _instance = None

    CATEGORIES = [
        "mobile screenshot",
        "desktop screenshot",
        "wallpaper",
        "application widget",
        "document",
        "camera photograph"
    ]

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance._initialize()

        return cls._instance

    def _initialize(self):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.processor = CLIPProcessor.from_pretrained(
            "openai/clip-vit-base-patch32"
        )

        self.model = CLIPModel.from_pretrained(
            "openai/clip-vit-base-patch32"
        ).to(self.device)

        self.model.eval()

    def _load_image(self, image):

        if isinstance(image, (str, Path)):
            image = Image.open(image).convert("RGB")

        return image

    @torch.no_grad()
    def predict(self, image):

        image = self._load_image(image)

        text = [f"a photo of {label}" for label in self.CATEGORIES]

        inputs = self.processor(
            text=text,
            images=image,
            return_tensors="pt",
            padding=True,
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        outputs = self.model(**inputs)

        logits = outputs.logits_per_image

        probabilities = logits.softmax(dim=1).cpu().numpy()[0]

        result = {}

        for label, score in zip(self.CATEGORIES, probabilities):

            result[label] = float(score)

        return result

    def predict_best(self, image):

        scores = self.predict(image)

        label = max(scores, key=scores.get)

        confidence = scores[label]

        return {

            "category": label,

            "confidence": round(confidence, 4),

            "scores": scores

        }


classifier = AIClassifier()