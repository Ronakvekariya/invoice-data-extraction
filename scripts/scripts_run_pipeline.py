"""Simple runner script to execute the pipeline end-to-end."""
import argparse
import json
from invoice_extraction import ocr_from_yolo, ner_from_ocr, finalize


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--yolo-json", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--tesseract-cmd", default=None)
    parser.add_argument("--spaCy-model", default="en_core_web_trf")
    parser.add_argument("--ocr-out", default="ocr_output.json")
    parser.add_argument("--ner-out", default="structured_output.json")
    parser.add_argument("--final-out", default="final_output.json")
    args = parser.parse_args()

    ocr = ocr_from_yolo(args.yolo_json, args.image, tesseract_cmd=args.tesseract_cmd)
    with open(args.ocr_out, "w") as f:
        json.dump(ocr, f, indent=4)
    print(f"OCR output saved to {args.ocr_out}")

    ner = ner_from_ocr(ocr, model=args.spaCy_model)
    with open(args.ner_out, "w") as f:
        json.dump(ner, f, indent=4)
    print(f"NER output saved to {args.ner_out}")

    final = finalize(ner)
    with open(args.final_out, "w") as f:
        json.dump(final, f, indent=4)
    print(f"Final output saved to {args.final_out}")


if __name__ == "__main__":
    main()