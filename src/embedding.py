"""
embedding.py
Day 22 -> get_embedding(): converts text into a vector using a local
           sentence-transformers model (no API key needed).
Day 23 -> cosine_similarity(): measures similarity between two vectors.
"""

from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL_NAME

# Loaded once and reused — loading the model is the expensive part,
# not generating individual embeddings.
_model = SentenceTransformer(EMBEDDING_MODEL_NAME)


def get_embedding(text: str) -> list[float]:
    """
    Converts a piece of text into an embedding vector.

    Args:
        text: the text to embed (a sentence, a chunk, or a query).

    Returns:
        A list of floats representing the text's embedding.
    """
    if not text or not text.strip():
        raise ValueError("Cannot embed empty text.")

    vector = _model.encode(text)
    return vector.tolist()


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """
    Embeds multiple texts at once — more efficient than calling
    get_embedding() in a loop for many chunks.
    """
    vectors = _model.encode(texts)
    return vectors.tolist()


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Day 23 — calculates cosine similarity between two vectors.
    Returns a value from -1 (opposite) to 1 (identical direction).

    Args:
        vec_a: first vector.
        vec_b: second vector.

    Returns:
        The cosine similarity score.
    """
    import math

    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimensions to compare.")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)