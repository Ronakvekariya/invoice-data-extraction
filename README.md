# Intelligent Invoice Data Extraction

An end-to-end invoice document-processing pipeline that combines **YOLOv8 field detection, OCR, named-entity recognition, and rule-based post-processing** to convert invoice images into structured JSON.

## Pipeline

```text
Invoice image
      ↓
YOLOv8 field detection
      ↓
Bounding-box crops
      ↓
Tesseract OCR
      ↓
spaCy NER
      ↓
Rule-based normalization
      ↓
Structured JSON
```

## What it demonstrates

- Object detection for locating invoice fields.
- OCR for reading text from detected regions.
- NLP/NER for extracting semantic information.
- Rule-based normalization into a stable JSON schema.
- Modular Python code with a reusable package and CLI runner.
- Automated tests and GitHub Actions CI.

## Extracted information

The current normalization layer supports invoice identifiers, dates, due dates, totals, subtotal, tax/GST, seller details, buyer details, and GSTIN fields.

## Repository structure

```text
.
├── src/invoice_extraction/
│   ├── __init__.py
│   ├── ocr.py
│   ├── ner.py
│   └── postproc.py
├── scripts/
│   └── run_pipeline.py
├── tests/
│   └── test_postproc.py
├── notebooks/
├── examples/
├── data/                    # local datasets, ignored by Git
├── .github/workflows/ci.yml
├── main.py                  # YOLO training entry point
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Setup

Create a virtual environment and install the project:

```bash
python -m venv .venv
pip install -e .
pip install pytest
```

Install the spaCy transformer model:

```bash
python -m spacy download en_core_web_trf
```

Install Tesseract OCR separately.

## Run inference

Prepare YOLO detection output in JSON format, then run:

```bash
python scripts/run_pipeline.py \
  --yolo-json path/to/output.json \
  --image examples/Inv1.jpg \
  --ocr-out ocr_output.json \
  --ner-out structured_output.json \
  --final-out final_output.json
```

On Windows, pass the Tesseract executable path when needed:

```text
--tesseract-cmd "C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## Train the detector

The training entry point is configurable:

```bash
python main.py --data path/to/dataset.yaml --epochs 1 --imgsz 640 --batch 16
```

The training dataset and large model artifacts are intentionally kept out of the public repository when they are not needed for code review.

## Tests

```bash
pytest -q
```

The current tests focus on deterministic post-processing helpers, so they do not require Tesseract, spaCy, or the YOLO model to be installed for test execution.

## Example output

The repository contains synthetic/demo invoices. Example output values are illustrative:

```json
{
  "Invoice Id": "INV-1024",
  "Date": "12/01/2025",
  "Due Date": "20/01/2025",
  "Total": "1800.00 EUR",
  "Seller Name": "ABC Traders",
  "Buyer": "XYZ Retail"
}
```

## Evaluation

The original project reported approximately **93% field-extraction accuracy** on its available invoice template set. This is a project-specific result and is not presented as a general benchmark.

## Limitations and next steps

This remains a prototype rather than a production invoice-extraction service. The next engineering improvements are:

- reproducible field-level benchmarks;
- confidence scores and validation rules;
- more robust multi-template extraction;
- model/data versioning;
- an API service around inference;
- containerized deployment;
- broader integration tests.

## License

MIT

## Author

Ronak Vekariya
