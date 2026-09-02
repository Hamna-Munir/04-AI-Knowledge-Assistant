# Day 24 — Vector Database

**Objective:** Learn to efficiently store and search embeddings using a proper vector database, instead of holding everything in memory and comparing manually.

---

## 📖 Theory

### What is a vector database?

A **vector database** is a database purpose-built to store embeddings (vectors) and quickly find the most similar ones to a given query vector. Unlike a regular database — which is optimized for exact matches and structured queries (`WHERE id = 5`) — a vector database is optimized for **similarity search**: "find the vectors closest to this one."

### Why a normal database isn't enough for semantic search

A regular SQL or NoSQL database has no built-in concept of "closeness" between rows. To find similar vectors using a normal database, you'd have to fetch every row and manually calculate similarity in application code (exactly what Day 23 did, one comparison at a time) — this doesn't scale past a small number of documents. Vector databases use specialized indexing structures internally to make similarity search fast, even across millions of vectors.

### Vector storage

Vector storage means saving each chunk's embedding (its vector) in a way the database can efficiently search later — typically alongside the original text and any metadata needed to make the result useful.

### Metadata

Metadata is extra structured information stored alongside each vector — for example, which document a chunk came from, or which page number it appeared on. Metadata makes retrieved results actionable: without it, a search would return "here's a similar vector" with no way to trace it back to a specific source.

### Similarity search

This is the actual operation a vector database performs: given a query vector, return the top-K stored vectors that are most similar to it — the same concept from Day 23, but handled efficiently by the database itself instead of manual Python loops.

---

## 🛠️ Recommended Tool: ChromaDB

**ChromaDB** is used this week because it's simple, beginner-friendly, and runs locally without needing a separate server or cloud account — ideal for a learning project like this one.

---

## 📚 Reading

[ChromaDB Getting Started](https://docs.trychroma.com/getting-started) (official documentation)

---

## 💻 Coding Exercise

```bash
pip install chromadb
```

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection(name="pdf_chunks")

collection.add(
    documents=["chunk text here", "another chunk here"],
    metadatas=[
        {"page_number": 1, "document_name": "sample.pdf"},
        {"page_number": 2, "document_name": "sample.pdf"},
    ],
    ids=["chunk_1", "chunk_2"],
)
```

Build the pipeline:

```
Documents
   ↓
Chunks
   ↓
Embeddings
   ↓
ChromaDB
```

---

## 🛠 Mini Project

Store the Week 3 PDF's chunks in a ChromaDB vector database, with metadata for each chunk (`chunk` text, `page_number`, `document_name`).

---

## 🧠 Quiz

1. What is a vector database, in one sentence?
2. Why isn't a regular database sufficient for semantic search at scale?
3. Why is metadata useful alongside stored vectors?
4. Why is ChromaDB a reasonable choice for this week's learning project specifically?

*(Try answering from memory first, then check the theory section above.)*

---

## ⭐ Bonus

Store chunks from **multiple PDFs** in the same collection, using the `document_name` metadata field to tell them apart, and confirm retrieval can still correctly identify which document a result came from.

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Collection name problems | Reusing a collection name that already exists, or invalid characters in the name | Use `get_or_create_collection()` instead of `create_collection()`, or check the name follows ChromaDB's naming rules |
| Embedding dimensions mismatch | Chunks were embedded with a different model than the one the collection expects | Keep the embedding model consistent across the whole project |
| Duplicate IDs | Reusing the same `id` for two different chunks | Generate unique IDs (e.g., `f"{document_name}_chunk_{i}"`) for every chunk |
| Incorrect metadata | Metadata dictionary keys don't match what retrieval code expects later | Keep metadata field names consistent and documented (e.g., always `page_number`, not sometimes `page`) |

---

## ✅ Checklist

- [ ] ChromaDB installed
- [ ] Collection created
- [ ] Chunks stored
- [ ] Embeddings stored
- [ ] Metadata stored (chunk text, page number, document name)
- [ ] Git commit made

---

## 📂 Git Commit

```bash
git add .
git commit -m "feat: add vector database"
git push
```

---

## 📝 Journal

*Add Day 24's learning and biggest takeaway to `journal.md`.*
