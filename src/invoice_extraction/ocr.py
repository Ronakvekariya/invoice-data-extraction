"""OCR helpers for invoice field extraction."""

import json
from typing import Dict, Optional

import cv2
import pytesseract


def ocr_from_yolo(
    yolo_json_path: str,
    image_path: str,
    tesseract_cmd: Optional[str] = None,
) -> Dict[str, str]:
    """Read YOLO detections, crop detected regions, and run Tesseract OCR."""
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    with open(yolo_json_path, "r", encoding="utf-8") as file:
        detections = json.load(file)

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Invoice image not found: {image_path}")

    height, width = image.shape[:2]
    output: Dict[str, str] = {}

    for obj in detections:
        label = obj.get("label")
        box = obj.get("bounding_box") or obj.get("bbox")
        if not label or box is None:
            continue

        values = list(box.values()) if isinstance(box, dict) else list(box)
        if len(values) < 4:
            continue

        try:
            x1, y1, x2, y2 = map(int, values[:4])
        except (TypeError, ValueError):
            continue

        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(width, x2), min(height, y2)
        if x2 <= x1 or y2 <= y1:
            continue

        crop = image[y1:y2, x1:x2]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        output[label] = pytesseract.image_to_string(
            gray,
            config="--psm 6",
        ).strip()

    return output
