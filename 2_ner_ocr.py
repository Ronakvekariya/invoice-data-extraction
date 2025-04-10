import json
import spacy

# Load the transformer-based NER model
nlp = spacy.load("en_core_web_trf")

# Load extracted OCR data
with open("ocr_output.json", "r") as f:
    extracted_data = json.load(f)

structured_data = {}

# Apply NER for each extracted text field
for key, text in extracted_data.items():
    doc = nlp(text)
    structured_data[key] = {
        "text": text,
        "entities": [(ent.text, ent.label_) for ent in doc.ents]
    }

# Save structured data
with open("structured_output.json", "w") as f:
    json.dump(structured_data, f, indent=4)

print("NER processing complete. Data saved in structured_output.json")