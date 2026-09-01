# Day 23 — Vector Similarity

**Objective:** Understand how the system calculates similarity between two vectors — the math behind semantic search.

---

## 📖 Theory

### Vectors and dimensions

A vector is a list of numbers. The number of values in that list is its **dimensionality** — an embedding model might produce 384-dimensional or 1536-dimensional vectors, meaning each piece of text is represented by 384 or 1536 numbers. Every vector from the same embedding model has the same number of dimensions, which is what makes comparing them meaningful.

### Distance vs similarity

Two related but distinct ideas:

- **Distance** — how far apart two vectors are. Smaller distance = more similar.
- **Similarity** — a score (often between -1 and 1, or 0 and 1) representing how alike two vectors are. Higher similarity = more alike.

Different metrics calculate this differently — this week's focus is specifically on **cosine similarity**.

### Cosine similarity

Cosine similarity measures the angle between two vectors, rather than the straight-line distance between them. A cosine similarity of 1 means the vectors point in exactly the same direction (maximally similar); 0 means they're unrelated (perpendicular); -1 means they point in opposite directions.

```
cosine_similarity = (A · B) / (|A| × |B|)
```

Where `A · B` is the dot product of the two vectors, and `|A|`, `|B|` are their magnitudes (lengths).

### Why cosine similarity is useful for text

Text embeddings can vary in magnitude for reasons unrelated to meaning (e.g., longer text sometimes produces vectors with larger magnitude). Cosine similarity ignores magnitude entirely and focuses only on *direction* — which is exactly what captures meaning in embedding space. This makes it more reliable for comparing text embeddings than raw distance measures that are sensitive to vector length.

### Query vector

When a user asks a question, that question is embedded into a vector the same way document chunks were. This is the **query vector** — it gets compared against every stored chunk vector to find the most similar (i.e., most relevant) ones.

```
Query Vector
     ↓
Compare
     ↓
Document Vectors
     ↓
Most Similar
```

---

## 📚 Reading

[scikit-learn: Cosine similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html) (reference documentation)

---

## 💻 Coding Exercise

```python
sentences = [
    "I love machine learning.",
    "AI is fascinating.",
    "I like pizza.",
    "Deep learning is useful.",
]
query = "I enjoy studying AI."

query_vector = embedding_model.encode(query)
sentence_vectors = [embedding_model.encode(s) for s in sentences]

for sentence, vector in zip(sentences, sentence_vectors):
    score = cosine_similarity(query_vector, vector)
    print(f"{score:.3f}  —  {sentence}")
```

**Expected pattern:** "I love machine learning." and "Deep learning is useful." should score noticeably higher than "I like pizza." — even though none of them share the exact words in the query.

---

## 🛠 Mini Project

Implement similarity calculation between the query and the PDF chunks from Week 3, replacing the naive keyword-overlap scoring used there.

---

## 🧠 Quiz

1. What does cosine similarity actually measure — distance or angle?
2. What does a cosine similarity score close to 1 mean? Close to 0?
3. What is a query vector, and where does it come from?
4. Why is cosine similarity preferred over raw distance for comparing text embeddings?

*(Try answering from memory first, then check the theory section above.)*

---

## ⭐ Bonus

Return the **top 3 most similar chunks** for a given query, sorted by similarity score (highest first), instead of just the single best match.

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Comparing vectors of different dimensions | Query and document chunks were embedded using two different models | Always use the exact same embedding model for both the query and the documents |
| Empty embeddings | Passed empty or whitespace-only text to the embedding model | Validate/skip empty chunks before embedding them |
| Incorrect similarity calculation | Custom cosine similarity implementation has a bug (e.g., forgot to normalize) | Use a well-tested library function (e.g., `sklearn.metrics.pairwise.cosine_similarity`) instead of a manual implementation, or carefully verify the formula |

---

## ✅ Checklist

- [ ] Cosine similarity understood
- [ ] Query embedding created
- [ ] Chunk embeddings created
- [ ] Similarity calculated between query and chunks
- [ ] Top results returned
- [ ] Git commit made

---

## 📂 Git Commit

```bash
git add .
git commit -m "feat: add semantic similarity search"
git push
```

---

## 📝 Journal

*Add Day 23's learning and biggest takeaway to `journal.md`.*
