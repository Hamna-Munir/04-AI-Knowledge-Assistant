"""
retrieval.py
Day 25 — semantic retrieval: embeds the user's question and finds the
top-K most similar stored chunks, replacing Week 3's keyword matching.
"""

from src.vector_store import get_or_create_collection


def retrieve_relevant_chunks(query: str, top_k: int = 3, collection_name: str = "pdf_chunks") -> list[dict]:
    """
    Finds the top-K chunks most semantically similar to the query.

    Args:
        query: the user's question.
        top_k: how many chunks to retrieve.
        collection_name: which ChromaDB collection to search.

    Returns:
        A list of dicts, each with 'text', 'metadata', and 'distance'
        (lower distance = more similar), ordered by relevance.
    """
    collection = get_or_create_collection(collection_name)

    if collection.count() == 0:
        return []

    results = collection.query(query_texts=[query], n_results=min(top_k, collection.count()))

    retrieved = []
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for doc, metadata, distance in zip(documents, metadatas, distances):
        retrieved.append({
            "text": doc,
            "metadata": metadata,
            "distance": distance,
            # ChromaDB returns distance (lower = better); convert to a
            # similarity-style score (higher = better) for display.
            "similarity": 1 - distance,
        })

    return retrieved