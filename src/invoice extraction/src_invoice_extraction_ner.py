"""NER helpers: run spaCy NER over OCR output."""
from typing import Dict, Any
import json
import spacy


def ner_from_ocr(ocr_data: Dict[str, str], model: str = "en_core_web_trf") -> Dict[str, Any]:
    """Apply spaCy NER to each OCR field and return structured dict."""
    try:
        nlp = spacy.load(model)
    except Exception as e:
        raise RuntimeError(f"Failed to load spaCy model '{model}': {e}")

    structured: Dict[str, Any] = {}
    for key, text in ocr_data.items():
        doc = nlp(text or "")
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        structured[key] = {
            "text": text,
            "entities": entities,
        }

    return structured


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--ocr-in", default="ocr_output.json")
    parser.add_argument("--model", default="en_core_web_trf")
    parser.add_argument("--out", default="structured_output.json")
    args = parser.parse_args()

    with open(args.ocr_in, "r") as f:
        ocr_data = json.load(f)

    structured = ner_from_ocr(ocr_data, model=args.model)
    with open(args.out, "w") as f:
        json.dump(structured, f, indent=4)

    print(f"NER output written to {args.out}")