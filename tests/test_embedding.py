"""
tests/test_embedding.py
Tests for embedding.py — Day 22 (embeddings) and Day 23 (similarity).

Run with:
    pytest tests/test_embedding.py -v

Note: loading the sentence-transformers model takes a few seconds on
first run (and downloads it the very first time).
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from src.embedding import get_embedding, cosine_similarity


def test_get_embedding_returns_vector():
    vector = get_embedding("Hello world.")
    assert isinstance(vector, list)
    assert len(vector) > 0
    assert all(isinstance(x, float) for x in vector)


def test_get_embedding_empty_text_raises():
    with pytest.raises(ValueError):
        get_embedding("")


def test_get_embedding_whitespace_only_raises():
    with pytest.raises(ValueError):
        get_embedding("   ")


def test_cosine_similarity_identical_vectors():
    vec = [1.0, 2.0, 3.0]
    assert cosine_similarity(vec, vec) == pytest.approx(1.0, abs=1e-6)


def test_cosine_similarity_orthogonal_vectors():
    vec_a = [1.0, 0.0]
    vec_b = [0.0, 1.0]
    assert cosine_similarity(vec_a, vec_b) == pytest.approx(0.0, abs=1e-6)


def test_cosine_similarity_dimension_mismatch_raises():
    with pytest.raises(ValueError):
        cosine_similarity([1.0, 2.0], [1.0, 2.0, 3.0])


def test_similar_sentences_score_higher_than_unrelated():
    # This is the core Day 22 example: different words, similar meaning
    vec_password = get_embedding("How do I reset my password?")
    vec_credentials = get_embedding("I forgot my login credentials.")
    vec_weather = get_embedding("What's the weather like today?")

    similar_score = cosine_similarity(vec_password, vec_credentials)
    unrelated_score = cosine_similarity(vec_password, vec_weather)

    assert similar_score > unrelated_score
