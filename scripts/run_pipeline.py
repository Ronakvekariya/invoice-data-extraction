"""Run the OCR → NER → normalization pipeline."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from invoice_extraction import finalize, ner_from_ocr, ocr_from_yolo  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run invoice OCR, NER, and normalization.",
    )
    parser.add_argument("--yolo-json", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--tesseract-cmd", default=None)
    parser.add_argument("--spacy-model", default="en_core_web_trf")
    parser.add_argument("--ocr-out", default="ocr_output.json")
    parser.add_argument("--ner-out", default="structured_output.json")
    parser.add_argument("--final-out", default="final_output.json")
    args = parser.parse_args()

    ocr = ocr_from_yolo(
        args.yolo_json,
        args.image,
        tesseract_cmd=args.tesseract_cmd,
    )
    Path(args.ocr_out).write_text(
        json.dumps(ocr, indent=4),
        encoding="utf-8",
    )

    ner = ner_from_ocr(ocr, model=args.spacy_model)
    Path(args.ner_out).write_text(
        json.dumps(ner, indent=4),
        encoding="utf-8",
    )

    final = finalize(ner)
    Path(args.final_out).write_text(
        json.dumps(final, indent=4),
        encoding="utf-8",
    )

    print(f"Final structured output written to {args.final_out}")


if __name__ == "__main__":
    main()
