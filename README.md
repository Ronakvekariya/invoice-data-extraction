# Intelligent Invoice Data Extraction

An end-to-end computer vision and NLP pipeline for extracting structured information from invoice documents.

This project combines YOLOv8-based field detection, OCR, named-entity recognition (NER), and post-processing logic to convert invoice images into structured JSON output for downstream business workflows.

## Overview

The project is designed to identify important invoice components such as:

- invoice number
- invoice date
- due date
- total amount
- subtotal
- tax
- seller name and address
- buyer details
- GST information

The pipeline works as follows:

Invoice image → YOLOv8 detection → bounding box cropping → OCR extraction → NER processing → rule-based normalization → structured JSON

## Why this project exists

This repository demonstrates how a practical invoice processing workflow can be built using:

- object detection for locating relevant invoice regions
- OCR for extracting text from detected boxes
- NLP for understanding field semantics
- rule-based post-processing for structured output generation

The project is useful for learning, experimentation, and building a foundation for a production invoice extraction system.

## Tech stack

- Python
- OpenCV
- Tesseract OCR
- Ultralytics YOLOv8
- spaCy
- spaCy transformer model
- JSON output

## Repository structure

```text
invoice-data-extraction/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── main.py
├── src/
│   └── invoice_extraction/
│       ├── __init__.py
│       ├── ocr.py
│       ├── ner.py
│       └── postproc.py
├── scripts/
│   └── run_pipeline.py
├── notebooks/
│   ├── main.ipynb
│   ├── main_small_dataset.ipynb
│   └── bb_to_str.ipynb
├── tests/
│   └── test_postproc.py
├── examples/
│   ├── Inv1.jpg
│   └── hdsample.jpg
├── .github/
│   └── workflows/
│       └── python.yml
├── data/
│   └── (gitignored raw and processed data)
└── results/
    └── generated JSON artifacts
```

## Project workflow

### 1. Training / detection stage
`main.py` is the YOLO-based training script. It uses a custom invoice dataset to detect invoice fields such as:

- total
- date
- seller name
- buyer
- tax
- subtotal
- GSTIN
- logo
- table
- etc.

### 2. OCR stage
`ocr.py` reads the YOLO output JSON and crops each detected bounding box from the invoice image. It then runs Tesseract OCR to extract text from each region.

### 3. NER stage
`ner.py` takes the OCR output and applies a spaCy NER model to assign semantic labels to extracted text.

### 4. Final structuring stage
`postproc.py` applies regex- and rule-based extraction to normalize the OCR/NER results into a final invoice JSON structure.

## Installation

### Prerequisites

- Python 3.9+
- Tesseract OCR installed on the system
- pip and virtual environment support

### Install dependencies

```bash
pip install -r requirements.txt
```

### Install spaCy transformer model

```bash
python -m spacy download en_core_web_trf
```

### Install Tesseract OCR

#### Windows
Download and install Tesseract from:
https://github.com/UB-Mannheim/tesseract/wiki

Then update the OCR path if needed in the code.

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr
```

#### macOS
```bash
brew install tesseract
```

## Setup for local execution

### Option 1: Run the pipeline using the wrapper script

```bash
PYTHONPATH=$PWD:$PWD/src python scripts/run_pipeline.py \
  --yolo-json output.json \
  --image path/to/invoice.jpg \
  --ocr-out ocr_output.json \
  --ner-out structured_output.json \
  --final-out final_output.json
```

### Option 2: Run the pipeline manually

```bash
python main.py
python src/invoice_extraction/ocr.py output.json path/to/invoice.jpg
python src/invoice_extraction/ner.py --ocr-in ocr_output.json --out structured_output.json
python src/invoice_extraction/postproc.py --in structured_output.json --out final_output.json
```

## Expected output format

The final output is JSON and typically looks like this:

```json
{
  "Invoice Id": "INV-1024",
  "Date": "12/01/2025",
  "Due Date": "20/01/2025",
  "Total": "₹1800.00",
  "Sub Total": "₹1500.00",
  "GST(18%)": "₹300.00",
  "Seller Name": "ABC Traders",
  "Seller Address": "123 Market Road, Bengaluru",
  "Buyer": "XYZ Retail Pvt Ltd",
  "GSTIN Buyer": "29ABCDE1234F1Z5",
  "GSTIN Seller": "29XYZAB5678C1Z3"
}
```

The exact values depend on the invoice source and the OCR/NER quality.

## Running tests

The project includes lightweight unit tests for the parsing and normalization logic.

```bash
pytest -q
```

## Notebook usage

The repository includes experimental notebook-based workflows for:

- invoice field detection
- OCR extraction
- post-processing
- model training

These notebooks are useful for prototyping and exploration. You may move them to a dedicated notebook directory or keep them in the root as working experiments.

## Configuration tips

Some project settings are hard-coded and may need adjustment when running on a new machine:

- Tesseract executable path
- dataset path
- image path
- spaCy model name
- output paths

A good next step is to refactor these values into environment variables or a configuration file.

## Roadmap

Planned improvements for this repository include:

- create a cleaner package structure
- add reusable config files
- add robust validation of extracted fields
- improve regex extraction for multiple invoice templates
- add type hints and dataclasses
- add CI/CD pipeline
- add package installation support
- build a lightweight API service around the pipeline
- add dataset versioning and reproducibility tools

## Limitations

This project is a research/prototype-style repository and not yet a production-ready invoice extraction service. It is best treated as:

- a learning project
- a demonstration pipeline
- a base for a more robust extraction engine

## License

This project is licensed under the MIT License unless otherwise specified.

## Author

Ronak Vekariya

GitHub: https://github.com/Ronakvekariya

## Acknowledgements

This project uses:

- Ultralytics YOLOv8
- OpenCV
- Tesseract OCR
- spaCy
- Python ecosystem libraries
