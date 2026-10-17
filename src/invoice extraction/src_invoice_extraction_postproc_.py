"""Postprocessing and normalization helpers."""
from typing import Any, Dict, List
import re


def extract_field(data: Dict[str, Any], possible_keys: List[str], default: str = "") -> str:
    for key in possible_keys:
        if key in data:
            text = data[key].get("text", "").strip()
            if text:
                return text
    return default


def extract_regex(text: str, pattern: str) -> str:
    if not text:
        return ""
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1) if match else ""


def format_date(date_str: str) -> str:
    if not date_str:
        return ""

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

    return date_str


def finalize(structured_data: Dict[str, Any]) -> Dict[str, Any]:
    final_data = {
        "Invoice Id": extract_regex(extract_field(structured_data, ["NUMBER", "INVOICE_ID"]), r"INVOICE\s*#?\s*([\w-]+)"),
        "Date": extract_regex(extract_field(structured_data, ["DATE", "INVOICE_DATE"]), r"(\d{1,2}[-/ ]\w+[-/ ]\d{2,4})"),
        "Total": extract_regex(extract_field(structured_data, ["TOTAL", "BALANCE_DUE", "GRAND_TOTAL"]), r"([\d.,]+\s?[A-Z]{3})"),
        "Due Date": extract_regex(extract_field(structured_data, ["DUE_DATE", "PAYMENT_DUE"]), r"(\d{1,2}[-/ ]\w+[-/ ]\d{2,4})"),
        "Sub Total": extract_regex(extract_field(structured_data, ["SUB_TOTAL", "NET_AMOUNT"]), r"([\d.,]+\s?[A-Z]{3})"),
        "GST(18%)": extract_regex(extract_field(structured_data, ["GST(18%)", "TAX"]), r":\s*([\d.,]+)"),
        "Seller Name": extract_field(structured_data, ["SELLER_NAME", "COMPANY_NAME"]),
        "Seller Address": extract_field(structured_data, ["SELLER_ADDRESS", "COMPANY_ADDRESS"]).replace("Address:", "").strip() if extract_field(structured_data, ["SELLER_ADDRESS", "COMPANY_ADDRESS"]) else "",
        "Buyer": extract_field(structured_data, ["BUYER", "CUSTOMER_NAME"]).replace("Bill to:", "").strip() if extract_field(structured_data, ["BUYER", "CUSTOMER_NAME"]) else "",
        "GSTIN Buyer": extract_regex(extract_field(structured_data, ["GSTIN_BUYER"]), r"(GSTIN\s*\d+\w+)"),
        "GSTIN Seller": extract_regex(extract_field(structured_data, ["GSTIN_SELLER"]), r"(GSTIN\s*\d+\w+)")
    }

    final_data["Date"] = format_date(final_data.get("Date", ""))
    final_data["Due Date"] = format_date(final_data.get("Due Date", ""))
    return final_data


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="infile", default="structured_output.json")
    parser.add_argument("--out", default="final_output.json")
    args = parser.parse_args()

    with open(args.infile, "r") as f:
        structured = json.load(f)

    final = finalize(structured)
    with open(args.out, "w") as f:
        json.dump(final, f, indent=4)

    print(f"Final structured data saved in {args.out}")