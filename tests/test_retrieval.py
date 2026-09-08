"""
tests/test_retrieval.py
Tests for vector_store.py and retrieval.py — Day 24 (vector DB) and
Day 25 (semantic retrieval).

Run with:
    pytest tests/test_retrieval.py -v
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.vector_store import store_chunks, clear_collection, get_or_create_collection
from src.retrieval import retrieve_relevant_chunks

TEST_COLLECTION = "test_pdf_chunks"


def setup_module(module):
    """Clear any leftover test data before running this file's tests."""
    clear_collection(TEST_COLLECTION)


def teardown_module(module):
    """Clean up after this file's tests run."""
    clear_collection(TEST_COLLECTION)


def test_store_chunks_and_retrieve():
    chunks = [
        "Employees can request annual leave through the HR portal.",
        "The company offers a 401k match of up to 4%.",
        "All laptops must be returned upon termination of employment.",
    ]
    store_chunks(chunks, document_name="test_doc.pdf", collection_name=TEST_COLLECTION)

    collection = get_or_create_collection(TEST_COLLECTION)
    assert collection.count() == 3


def test_semantic_retrieval_finds_related_meaning_different_words():
    # This is the Day 27 example from the curriculum: the question uses
    # completely different words than the document, but means the same thing.
    chunks = ["Employees can request annual leave through the HR portal."]
    clear_collection(TEST_COLLECTION)
    store_chunks(chunks, document_name="test_doc.pdf", collection_name=TEST_COLLECTION)

    results = retrieve_relevant_chunks(
        "Where should staff apply for vacation?", top_k=1, collection_name=TEST_COLLECTION
    )

    assert len(results) == 1
    assert "annual leave" in results[0]["text"].lower()


def test_retrieve_returns_empty_list_when_collection_empty():
    clear_collection(TEST_COLLECTION)
    results = retrieve_relevant_chunks("any question", collection_name=TEST_COLLECTION)
    assert results == []


def test_retrieve_respects_top_k():
    chunks = [f"This is test chunk number {i}." for i in range(5)]
    clear_collection(TEST_COLLECTION)
    store_chunks(chunks, document_name="test_doc.pdf", collection_name=TEST_COLLECTION)

    results = retrieve_relevant_chunks("test chunk", top_k=2, collection_name=TEST_COLLECTION)
    assert len(results) == 2


def test_retrieve_includes_similarity_and_metadata():
    chunks = ["A short test chunk about refunds."]
    clear_collection(TEST_COLLECTION)
    store_chunks(chunks, document_name="test_doc.pdf", collection_name=TEST_COLLECTION)

    results = retrieve_relevant_chunks("refund policy", top_k=1, collection_name=TEST_COLLECTION)

    assert "similarity" in results[0]
    assert "metadata" in results[0]
    assert results[0]["metadata"]["document_name"] == "test_doc.pdf"