import json
import cv2
import pytesseract

# Set the Tesseract OCR path (For Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load YOLO JSON output
with open("output.json", "r") as f:
    yolo_data = json.load(f)

# Read the invoice image
image_path = "dataset_small/images/test/Template33_Instance13.jpg"
image = cv2.imread(image_path)

# Extract text from each bounding box
extracted_data = {}
for obj in yolo_data:
    label = obj['label']  # Extract label (e.g., "TOTAL", "DATE")
    x1, y1, x2, y2 = map(int, obj['bounding_box'].values())  # Bounding box coordinates

    # Crop the bounding box region
    cropped_img = image[y1:y2, x1:x2]

    # Convert to grayscale (improves OCR accuracy)
    gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

    # Apply Tesseract OCR to extract text
    extracted_text = pytesseract.image_to_string(gray, config="--psm 6").strip()

    # Store extracted text with label
    extracted_data[label] = extracted_text

# Save extracted text in JSON format
with open("ocr_output.json", "w") as f:
    json.dump(extracted_data, f, indent=4)

print("OCR extraction complete. Data saved in ocr_output.json")
