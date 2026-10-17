"""OCR helpers for detected invoice fields."""

import json
from pathlib import Path
from typing import Dict, Optional

import cv2
import pytesseract


def ocr_from_yolo(
    yolo_json_path: str,
    image_path: str,
    tesseract_cmd: Optional[str] = None,
) -> Dict[str, str]:
    """Read YOLO detections, crop invoice regions, and run Tesseract OCR."""
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    with Path(yolo_json_path).open("r", encoding="utf-8") as file:
        yolo_data = json.load(file)

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Invoice image not found: {image_path}")

    height, width = image.shape[:2]
    extracted_data: Dict[str, str] = {}

    for obj in yolo_data:
        label = obj.get("label")
        bounding_box = obj.get("bounding_box") or obj.get("bbox")

        if not label or bounding_box is None:
            continue

        if isinstance(bounding_box, dict):
            values = list(bounding_box.values())
        elif isinstance(bounding_box, (list, tuple)):
            values = list(bounding_box)
        else:
            continue

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

        cropped = image[y1:y2, x1:x2]
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        extracted_data[label] = pytesseract.image_to_string(
            gray,
            config="--psm 6",
        ).strip()

    return extracted_data
