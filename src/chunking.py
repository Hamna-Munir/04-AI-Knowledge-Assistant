"""
chunking.py
chunk_text() reused from Week 3. Week 3's keyword-based
select_relevant_chunks() has been replaced entirely by semantic
retrieval (see retrieval.py) — that's the core upgrade this week.
"""


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """
    Splits text into overlapping chunks.

    Args:
        text: the full extracted document text.
        chunk_size: max characters per chunk.
        overlap: characters shared between consecutive chunks.

    Returns:
        A list of text chunks.
    """
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks