"""
AI Classification Labels

These prompts are used by the Hugging Face
SigLIP/CLIP model for zero-shot image classification.
"""

CLASS_LABELS = [

    "a natural camera photograph",

    "a mobile phone screenshot",

    "a desktop screenshot",

    "a wallpaper or background image",

    "a mobile home screen",

    "a mobile application interface",

    "a widget on a mobile screen",

    "a scanned document",

    "a printed document",

    "a receipt",

    "an invoice",

    "a handwritten note",

    "a presentation slide",

    "a whiteboard",

    "a chart",

    "a graph",

    "an icon",

    "a logo"

]


# ---------------------------------------------------------
# Mapping AI prompt -> Your project category
# ---------------------------------------------------------

LABEL_MAPPING = {

    "a natural camera photograph": "camera",

    "a mobile phone screenshot": "screenshot",

    "a desktop screenshot": "screenshot",

    "a wallpaper or background image": "wallpaper",

    "a mobile home screen": "screenshot",

    "a mobile application interface": "screenshot",

    "a widget on a mobile screen": "widget",

    "a scanned document": "document",

    "a printed document": "document",

    "a receipt": "document",

    "an invoice": "document",

    "a handwritten note": "document",

    "a presentation slide": "document",

    "a whiteboard": "document",

    "a chart": "document",

    "a graph": "document",

    "an icon": "widget",

    "a logo": "widget"

}