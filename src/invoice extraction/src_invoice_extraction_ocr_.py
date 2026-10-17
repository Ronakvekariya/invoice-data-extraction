"""OCR helpers: read YOLO JSON, crop image regions and run Tesseract OCR."""
from typing import Dict
import json
import cv2
import pytesseract


def ocr_from_yolo(yolo_json_path: str, image_path: str, tesseract_cmd: str = None) -> Dict[str, str]:
    """Read YOLO JSON file and an image, crop detected boxes and return OCR text per label."""
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    with open(yolo_json_path, "r") as f:
        yolo_data = json.load(f)

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    extracted_data: Dict[str, str] = {}

    for obj in yolo_data:
        label = obj.get("label")
        bb = obj.get("bounding_box") or obj.get("bbox") or {}

        if isinstance(bb, dict):
            try:
                x1, y1, x2, y2 = map(int, bb.values())
            except Exception:
                vals = list(bb.values())
                if len(vals) >= 4:
                    x1, y1, x2, y2 = map(int, vals[:4])
                else:
                    continue
        elif isinstance(bb, (list, tuple)) and len(bb) >= 4:
            x1, y1, x2, y2 = map(int, bb[:4])
        else:
            continue

        h, w = image.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)

        if x2 <= x1 or y2 <= y1:
            continue

        cropped = image[y1:y2, x1:x2]
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray, config="--psm 6").strip()
        extracted_data[label] = text

    return extracted_data


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("yolo_json")
    parser.add_argument("image")
    parser.add_argument("--tesseract-cmd", default=None)
    parser.add_argument("--out", default="ocr_output.json")
    args = parser.parse_args()

    out = ocr_from_yolo(args.yolo_json, args.image, args.tesseract_cmd)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=4)

    print(f"OCR output written to {args.out}")