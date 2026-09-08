"""
vector_store.py
Day 24 — stores document chunks (with embeddings + metadata) in ChromaDB,
and provides the underlying query interface used by retrieval.py.
"""

import chromadb
from src.embedding import get_embeddings_batch, get_embedding

# In-memory ChromaDB client — resets each session. Good enough for this
# week's learning project; persisting across sessions is a Future
# Improvement noted in the README.
_client = chromadb.Client()


def get_or_create_collection(name: str = "pdf_chunks"):
    """
    Returns the ChromaDB collection, creating it if it doesn't exist yet.

    Explicitly configured to use cosine similarity (hnsw:space) instead
    of ChromaDB's default L2/Euclidean distance — without this, the
    "similarity" scores shown in the UI come out wrong (near-zero or
    negative) because 1 - L2_distance isn't a valid similarity score.
    """
    return _client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"},
    )


def store_chunks(chunks: list[str], document_name: str, collection_name: str = "pdf_chunks"):
    """
    Embeds and stores a list of text chunks in ChromaDB, with metadata
    identifying which document and (approximate) page each came from.

    Args:
        chunks: list of text chunks (from chunking.chunk_text()).
        document_name: name of the source PDF, stored as metadata.
        collection_name: which ChromaDB collection to store into.
    """
    if not chunks:
        return

    collection = get_or_create_collection(collection_name)
    embeddings = get_embeddings_batch(chunks)

    ids = [f"{document_name}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [
        {"document_name": document_name, "chunk_index": i}
        for i in range(len(chunks))
    ]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )


def clear_collection(collection_name: str = "pdf_chunks"):
    """Removes all chunks from a collection — used when a new PDF is uploaded."""
    try:
        _client.delete_collection(name=collection_name)
    except Exception:
        pass  # collection didn't exist yet — nothing to clear