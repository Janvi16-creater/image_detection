"""
AI Image Classifier

Batch inference using HuggingFace SigLIP.

The model is loaded only once.
Multiple uncertain images are classified
in one forward pass.
"""

from pathlib import Path

import torch
from PIL import Image

from transformers import SiglipModel
from transformers import AutoProcessor
from config import MODEL_NAME

from classification.ai.prompts import (
    CLASS_LABELS,
    LABEL_MAPPING
)


class AIClassifier:

    def __init__(self):

        print("\nLoading HuggingFace SigLIP...")

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.processor = AutoProcessor.from_pretrained(
            MODEL_NAME
        )

        self.model = SiglipModel.from_pretrained(
            MODEL_NAME
        )

        self.model.to(self.device)

        self.model.eval()

        print(f"Model Loaded ({self.device})")

    # ---------------------------------------------------------

    @torch.no_grad()
    def classify(self, image_path):
        """
        Backward compatible.
        """

        return self.classify_batch(
            [image_path]
        )[0]

    # ---------------------------------------------------------

    @torch.no_grad()
    def classify_batch(self, image_paths):
        """
        Batch inference.

        Parameters
        ----------
        image_paths : list[Path]

        Returns
        -------
        list
        """

        if len(image_paths) == 0:
            return []

        images = []

        for path in image_paths:

            images.append(
                Image.open(path).convert("RGB")
            )

        inputs = self.processor(

            text=CLASS_LABELS,

            images=images,

            padding=True,

            return_tensors="pt"

        )

        inputs = {

            k: v.to(self.device)

            for k, v in inputs.items()

        }

        outputs = self.model(**inputs)

        probs = outputs.logits_per_image.softmax(dim=1)

        results = []

        for row in probs:

            confidence, idx = row.max(dim=0)

            prompt = CLASS_LABELS[idx.item()]

            results.append({

                "category": LABEL_MAPPING[prompt],

                "confidence": round(
                    confidence.item(),
                    3
                ),

                "prompt": prompt,

                "scores": {

                    CLASS_LABELS[i]:

                    round(
                        row[i].item(),
                        4
                    )

                    for i in range(
                        len(CLASS_LABELS)
                    )

                },

                "source": "huggingface"

            })

        return results


ai_classifier = AIClassifier()