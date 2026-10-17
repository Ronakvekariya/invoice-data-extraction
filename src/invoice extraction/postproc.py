import json
import re


# Load structured data from OCR + NER output
with open("structured_output.json", "r") as f:
    structured_data = json.load(f)

# Helper function to extract key values dynamically
def extract_field(data, possible_keys, default=""):
    """Tries multiple keys to find the correct value in extracted OCR output."""
    for key in possible_keys:
        if key in data:
            text = data[key].get("text", "").strip()
            if text:
                return text
    return default

# Regex-based field extraction
def extract_regex(text, pattern):
    """Extracts the first match of the given regex pattern from text."""
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1) if match else ""

# Define the final structured output
final_data = {
    "Invoice Id": extract_regex(extract_field(structured_data, ["NUMBER", "INVOICE_ID"]), r"INVOICE\s*#?\s*([\w-]+)"),
    "Date": extract_regex(extract_field(structured_data, ["DATE", "INVOICE_DATE"]), r"(\d{1,2}[-/ ]\w+[-/ ]\d{2,4})"),
    "Total": extract_regex(extract_field(structured_data, ["TOTAL", "BALANCE_DUE", "GRAND_TOTAL"]), r"([\d.,]+\s?[A-Z]{3})"),
    "Due Date": extract_regex(extract_field(structured_data, ["DUE_DATE", "PAYMENT_DUE"]), r"(\d{1,2}[-/ ]\w+[-/ ]\d{2,4})"),
    "Sub Total": extract_regex(extract_field(structured_data, ["SUB_TOTAL", "NET_AMOUNT"]), r"([\d.,]+\s?[A-Z]{3})"),
    "GST(18%)": extract_regex(extract_field(structured_data, ["GST(18%)", "TAX"]), r":\s*([\d.,]+)"),
    "Seller Name": extract_field(structured_data, ["SELLER_NAME", "COMPANY_NAME"]),
    "Seller Address": extract_field(structured_data, ["SELLER_ADDRESS", "COMPANY_ADDRESS"]).replace("Address:", "").strip(),
    "Buyer": extract_field(structured_data, ["BUYER", "CUSTOMER_NAME"]).replace("Bill to:", "").strip(),
    "GSTIN Buyer": extract_regex(extract_field(structured_data, ["GSTIN_BUYER"]), r"(GSTIN\s*\d+\w+)"),
    "GSTIN Seller": extract_regex(extract_field(structured_data, ["GSTIN_SELLER"]), r"(GSTIN\s*\d+\w+)")
}

# Save final structured output
with open("final_output.json", "w") as f:
    json.dump(final_data, f, indent=4)

print("Final structured data saved in final_output.json")


# Convert date formats if necessary
def format_date(date_str):
    if not date_str:
        return None
    match = re.search(r"(\d{1,2})[-/ ]([A-Za-z]+|\d{1,2})[-/ ](\d{2,4})", date_str)
    if match:
        day, month, year = match.groups()
        month = month if month.isdigit() else {
            "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
            "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
            "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
        }.get(month[:3], month)
        year = "20" + year if len(year) == 2 else year
        return f"{day}/{month}/{year}"
    return date_str  # Return as is if format is unknown

# Apply date formatting
final_data["Date"] = format_date(final_data["Date"])
final_data["Due Date"] = format_date(final_data["Due Date"])

# Save final structured output
with open("final_output.json", "w") as f:
    json.dump(final_data, f, indent=4)

print("Final structured data saved in final_output.json")
