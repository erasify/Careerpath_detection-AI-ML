"""
extractor/
──────────
Public API for the resume extraction package.

Usage:
    from extractor import extract_resume

    data = extract_resume("resume.pdf", api_key="YOUR_GEMINI_KEY")
    # or without API key (regex fallback):
    data = extract_resume("resume.pdf")
"""

from .text_reader import extract_text
from .gemini_parser import extract_with_gemini
from .regex_parser import extract_basic_regex


def extract_resume(file_path: str, api_key: str | None = None) -> dict:
    """
    Full extraction pipeline for a single resume file.

    1. Read raw text from PDF / DOCX / TXT
    2. If api_key provided → use Gemini AI (rich, structured output)
       Otherwise            → use regex fallback (offline, limited)

    Returns a raw dict in the standard resume schema.
    Raises ValueError if the file format is unsupported.
    """
    text = extract_text(file_path)
    if not text.strip():
        raise ValueError(f"No readable text found in: {file_path}")

    if api_key:
        try:
            return extract_with_gemini(text, api_key)
        except Exception as e:
            print(f"  ⚠  Gemini failed ({e}) — falling back to regex extractor.")

    return extract_basic_regex(text)
