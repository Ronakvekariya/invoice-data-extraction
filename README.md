# Intelligent Invoice Data Extraction

An end-to-end computer vision and NLP pipeline that converts invoice images into structured JSON data.

## Overview

The project combines object detection, OCR, named-entity recognition, and rule-based post-processing to extract important invoice fields such as invoice number, dates, totals, tax information, seller details, and buyer details.

The main pipeline is:

`Invoice image → YOLOv8 field detection → image cropping → Tesseract OCR → spaCy Transformer NER → regex / post-processing → structured JSON`

## What this project demonstrates

- **Computer vision:** locating relevant invoice regions with YOLOv8.
- **OCR:** extracting text from detected regions with Tesseract.
- **NLP:** processing OCR output with a transformer-based spaCy NER model.
- **Information extraction:** converting noisy text into a consistent JSON schema.
- **Pipeline thinking:** separating detection, OCR, NLP, and final normalization into individual stages.

## Repository structure

| File | Purpose |
| --- | --- |
| `main.py` | YOLOv8 training entry point. |
| `1_bb_ocr.py` | Reads detection output, crops regions, and performs OCR. |
| `2_ner_ocr.py` | Runs transformer-based NER over OCR results. |
| `3_final_structure_data.py` | Applies field-specific rules and creates final JSON output. |
| `output.json` / `ocr_output.json` / `structured_output.json` / `final_output.json` | Intermediate and final pipeline outputs. |

## Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Tesseract OCR

Tesseract must be installed separately because `pytesseract` is a Python wrapper around the OCR engine.

The current code contains a Windows-specific Tesseract path. For another machine, update that configuration before running the OCR stage.

### 3. Install the spaCy transformer model

```bash
python -m spacy download en_core_web_trf
```

### 4. Prepare the YOLO dataset

The training script expects a YOLO dataset configuration file and image/label directories. Update the paths in `main.py` for your local dataset layout.

## Running the pipeline

Run the stages in order:

```bash
python main.py
python 1_bb_ocr.py
python 2_ner_ocr.py
python 3_final_structure_data.py
```

The stages communicate through JSON files, making it easy to inspect intermediate results and debug individual components.

## Output schema

The final JSON is designed around invoice fields such as:

- Invoice ID
- Invoice date
- Due date
- Total
- Subtotal
- Tax
- Seller name and address
- Buyer
- Buyer / seller GST information

## Evaluation

The original project evaluation reported approximately **93% field-extraction accuracy** on its available invoice template set. This should be treated as a dataset-specific result; the repository does not currently include a reproducible benchmark suite.

## Engineering notes

This repository is a project prototype rather than a production-ready service. The next engineering steps would be to:

- make all paths configurable;
- add automated validation and unit tests;
- version the training configuration and dataset metadata;
- replace intermediate-file coupling with typed pipeline interfaces;
- add confidence scores and field-level validation;
- package the pipeline behind an API;
- containerize the application and add CI.

## Technologies

**Python · YOLOv8 · OpenCV · Tesseract OCR · spaCy · NLP · NER · JSON**

## Author

**Ronak Vekariya**

[GitHub](https://github.com/Ronakvekariya)
