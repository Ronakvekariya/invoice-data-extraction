"""Named-entity recognition helpers for OCR output."""

import json
from typing import Any, Dict

import spacy


def ner_from_ocr(
    ocr_data: Dict[str, str],
    model: str = "en_core_web_trf",
) -> Dict[str, Any]:
    """Apply a spaCy NER model to each OCR field."""
    try:
        nlp = spacy.load(model)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to load spaCy model '{model}': {exc}"
        ) from exc

    structured: Dict[str, Any] = {}

    for key, text in ocr_data.items():
        doc = nlp(text or "")
        structured[key] = {
            "text": text,
            "entities": [(entity.text, entity.label_) for entity in doc.ents],
        }

    return structured


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run NER over OCR JSON.")
    parser.add_argument("--ocr-in", default="ocr_output.json")
    parser.add_argument("--model", default="en_core_web_trf")
    parser.add_argument("--out", default="structured_output.json")
    args = parser.parse_args()

    with open(args.ocr_in, "r", encoding="utf-8") as file:
        ocr_data = json.load(file)

    structured = ner_from_ocr(ocr_data, model=args.model)

    with open(args.out, "w", encoding="utf-8") as file:
        json.dump(structured, file, indent=4)

    print(f"NER output written to {args.out}")


if __name__ == "__main__":
    main()
