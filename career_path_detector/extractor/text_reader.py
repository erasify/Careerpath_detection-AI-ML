"""
extractor/text_reader.py
─────────────────────────
Handles raw text extraction from PDF, DOCX, and TXT resume files.
"""

from pathlib import Path


def extract_text_from_pdf(path: str) -> str:
    """Try pdfplumber first, fall back to pypdf."""
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        if text.strip():
            return text.strip()
    except ImportError:
        pass

    from pypdf import PdfReader
    reader = PdfReader(path)
    return "\n".join(
        page.extract_text() for page in reader.pages if page.extract_text()
    ).strip()


def extract_text_from_docx(path: str) -> str:
    """Extract paragraphs from a .docx file."""
    from docx import Document
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_text(path: str) -> str:
    """
    Dispatcher — detects file extension and calls the correct extractor.

    Supported formats: .pdf, .docx, .doc, .txt
    Raises ValueError for unsupported formats.
    """
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    if ext in (".docx", ".doc"):
        return extract_text_from_docx(path)
    if ext == ".txt":
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    raise ValueError(f"Unsupported format: {ext}. Use PDF, DOCX, or TXT.")
