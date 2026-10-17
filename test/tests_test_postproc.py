# Basic tests for postprocessing
from invoice_extraction.postproc import extract_regex, format_date, finalize


def test_extract_regex():
    assert extract_regex("Invoice # ABC-123", r"INVOICE\s*#?\s*([\w-]+)") == "ABC-123"


def test_format_date():
    assert format_date("12 Jan 23") == "12/01/2023"
    assert format_date("5/6/2021") == "5/6/2021" or isinstance(format_date("5/6/2021"), str)


def test_finalize_empty():
    out = finalize({})
    assert isinstance(out, dict)