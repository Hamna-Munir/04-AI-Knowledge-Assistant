# Day 25 — Semantic Retrieval

**Objective:** Build actual semantic search — replacing Week 3's keyword matching with real meaning-based retrieval.

---

## 📖 Theory

### Query embedding

Just like every document chunk was converted into an embedding (Day 22–24), the user's question also needs to be converted into an embedding before it can be compared against stored chunks. This is the **query embedding** — it must be generated using the exact same embedding model used for the chunks, or the comparison won't be meaningful.

### Similarity search (in a vector database)

Once the query is embedded, the vector database compares it against every stored chunk vector and returns the ones with the highest similarity — this is the same cosine similarity concept from Day 23, now handled efficiently by ChromaDB instead of a manual loop.

### Top-K retrieval

**Top-K** means retrieving the K most similar results, rather than just the single best match or every possible match. K is a tunable number — too small and relevant information might be missed; too large and irrelevant chunks dilute the context sent to the LLM later.

### Relevance

Relevance is whether a retrieved chunk actually helps answer the question — high similarity score is a strong signal of relevance, but not a guarantee. Retrieval quality is ultimately judged by whether the retrieved chunks *actually* contain what's needed to answer correctly, which is exactly what Day 27's evaluation exercise checks.

### The retrieval pipeline

```
User Question
      ↓
Embedding
      ↓
Vector Search
      ↓
Top-K Chunks
```

This is the full pipeline that replaces Week 3's `select_relevant_chunks()` keyword-matching function.

---

## 📚 Reading

[ChromaDB: Querying a collection](https://docs.trychroma.com/usage-guide#querying-a-collection) (official documentation)

---

## 💻 Coding Exercise

```python
query = "How can I reset my password?"

results = collection.query(
    query_texts=[query],
    n_results=3,
)

for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
    print(f"[{metadata['document_name']} · page {metadata['page_number']}]")
    print(doc)
    print()
```

```
Query
 ↓
Embedding
 ↓
Vector DB
 ↓
Top 3 relevant chunks
```

---

## 🛠 Mini Project

Replace Week 3's keyword-matching chunk selection with this semantic retrieval pipeline — the AI PDF Assistant's core context-selection logic now runs on meaning, not exact word overlap.

---

## 🧠 Quiz

1. What is a query embedding, and why must it use the same model as the document embeddings?
2. What does "Top-K" mean in retrieval?
3. What's the difference between a chunk having a high similarity score and a chunk actually being relevant?
4. In what situation would semantic search clearly outperform Week 3's keyword search?

*(Try answering from memory first, then check the theory section above.)*

---

## ⭐ Bonus

Display the **similarity score** alongside each retrieved chunk, not just the chunk text — this makes it possible to see *how* confident the retrieval was, not just what it returned.

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Irrelevant chunks returned | K set too high, pulling in weakly-related results just to fill the count | Lower K, or filter out results below a minimum similarity threshold |
| Too many chunks | Sending all Top-K results to the LLM without checking if they're actually all needed | Test smaller K values (e.g., 2–3) before assuming more is better |
| Too few chunks | K set too low for questions that genuinely need multiple pieces of context | Increase K for broader/summary-style questions specifically |
| Poor chunking | Retrieval finds a chunk, but it's cut off mid-sentence or missing surrounding context | Revisit Week 3's chunk size/overlap settings — retrieval quality depends on chunk quality |

---

## ✅ Checklist

- [ ] Query embedding generated
- [ ] Vector search implemented
- [ ] Top-K retrieval working
- [ ] Relevant chunks correctly returned for a real question
- [ ] Git commit made

---

## 📂 Git Commit

```bash
git add .
git commit -m "feat: implement semantic retrieval"
git push
```

---

## 📝 Journal

*Add Day 25's learning and biggest takeaway to `journal.md`.*
