# Day 26 — RAG Pipeline Basics

**Objective:** Connect embeddings and retrieval to the LLM — completing the full Retrieval-Augmented Generation pipeline.

---

## 📖 Theory

### RAG = Retrieval-Augmented Generation

RAG is the pattern this entire week has been building toward: instead of relying only on an LLM's built-in training knowledge, the system first **retrieves** relevant information (via semantic search) and then **generates** an answer using that retrieved information as context. This is the same Context + Question prompt pattern from Week 3 (Day 17) — but now the context is selected via real semantic search instead of the whole document or basic keyword matching.

### The full RAG flow

```
Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Relevant Chunks
   ↓
Prompt + Context
   ↓
LLM
   ↓
Answer
```

Each stage of this flow was built individually across the week: embeddings (Day 22), similarity (Day 23), storage (Day 24), and retrieval (Day 25). Day 26 is where they all connect into one working pipeline.

### Retrieval vs generation

These are two distinct stages with different jobs:

- **Retrieval** — finding the *right information* (semantic search over stored chunks)
- **Generation** — producing a *coherent answer* using that information (the LLM call)

Retrieval quality has a direct ceiling effect on generation quality: if retrieval returns the wrong chunks, no amount of clever prompting can make the LLM's answer correct — the model can only work with what it's given.

### Where embeddings are used in RAG

Embeddings are used at two points: once (in advance) to embed all document chunks when building the vector database, and once (per request) to embed the user's question so it can be compared against those stored chunks. Both embeddings must come from the same model for the comparison to be meaningful (as established on Day 25).

---

## 📚 Reading

[Pinecone: What is Retrieval-Augmented Generation?](https://www.pinecone.io/learn/retrieval-augmented-generation/) (conceptual reference — RAG pattern, not tied to a specific vector DB provider)

---

## 💻 Coding Exercise

```python
def answer_with_rag(question: str, collection, top_k: int = 3) -> str:
    results = collection.query(query_texts=[question], n_results=top_k)
    retrieved_chunks = results["documents"][0]

    context = "\n\n".join(retrieved_chunks)
    prompt = build_qa_prompt(context, question)  # same pattern as Week 3, Day 17

    return get_answer(prompt)
```

---

## 🛠 Mini Project

Build the AI Knowledge Assistant's core Q&A pipeline:

```
User: "What does this document say about X?"

System:
Question
 ↓
Retrieve relevant information
 ↓
Give context to LLM
 ↓
Generate answer
```

---

## 🧠 Quiz

1. What does RAG stand for, and what are its two stages?
2. Why can't clever prompting fix a wrong answer caused by bad retrieval?
3. At which two points in the pipeline are embeddings actually used?
4. How does this week's RAG pipeline differ from Week 3's basic PDF Q&A pipeline?

*(Try answering from memory first, then check the theory section above.)*

---

## ⭐ Bonus

Display the **source/page number** alongside the generated answer, using the metadata stored with each chunk (Day 24) — so the user can see exactly where the answer came from, not just trust it blindly.

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Context too large | Too many/too long chunks retrieved and joined into one prompt | Lower `top_k`, or trim chunk length before joining |
| Wrong chunks retrieved | Embedding model mismatch, or `top_k` too low/high for the question type | Revisit Day 25's retrieval tuning |
| LLM ignores context | Grounding instruction (Week 3, Day 19) not applied to this pipeline | Reuse the same grounded system prompt from Week 3 |
| Missing source metadata | Metadata wasn't stored with the chunk, or wasn't carried through to the final answer display | Confirm metadata is present at storage time (Day 24) and passed through to the UI |

---

## ✅ Checklist

- [ ] Retrieval connected to LLM
- [ ] Retrieved context passed into the prompt
- [ ] Answers generated using retrieved context
- [ ] Sources displayed alongside answers
- [ ] Git commit made

---

## 📂 Git Commit

```bash
git add .
git commit -m "feat: build basic RAG pipeline"
git push
```

---

## 📝 Journal

*Add Day 26's learning and biggest takeaway to `journal.md`.*
