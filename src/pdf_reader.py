"""
pdf_reader.py
Reused from Week 3: extracts text from PDFs and detects empty/scanned PDFs.
"""

from pypdf import PdfReader


def extract_text_from_pdf(file) -> tuple[str, int]:
    """
    Extracts all text from a PDF.

    Args:
        file: a file path (str) OR a file-like object (e.g. from
              st.file_uploader) that pypdf.PdfReader can accept directly.

    Returns:
        A tuple of (full_extracted_text, total_pages).
    """
    reader = PdfReader(file)
    total_pages = len(reader.pages)

    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        full_text += page_text + "\n"

    return full_text.strip(), total_pages


def is_pdf_readable(extracted_text: str, min_chars: int = 20) -> bool:
    """Basic check to catch empty or scanned (image-only) PDFs."""
    return len(extracted_text.strip()) >= min_chars