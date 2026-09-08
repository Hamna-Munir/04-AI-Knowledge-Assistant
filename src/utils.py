"""
utils.py
Small helper functions shared across the app.
"""


def format_preview(text: str, max_chars: int = 500) -> str:
    """Returns a short preview of text, truncated with an ellipsis if long."""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."


def is_supported_file(filename: str) -> bool:
    """Extra validation beyond the Streamlit uploader's `type` filter."""
    return filename.lower().endswith(".pdf")