# Week 04 Summary — Semantic Search & Vector Retrieval

**Repository:** 04-AI-Knowledge-Assistant
**Days covered:** Day 22 – Day 28

---

## 🎯 Goal Recap

Replace Week 3's basic keyword-matching context selection with real **semantic search** — converting text into embeddings, storing them in a vector database, and retrieving relevant information by *meaning*, not exact word overlap. This is the foundational pattern behind Retrieval-Augmented Generation (RAG), used across most production document-AI systems.

---

## ✅ What Was Built

**AI Knowledge Assistant v1.0** — a full RAG pipeline wrapped in a custom chat-style Streamlit interface:

- Extracts and chunks PDF text (reused from Week 3)
- Converts chunks into embeddings using a local `sentence-transformers` model
- Stores embeddings + metadata (document name, chunk index) in a ChromaDB vector database
- Embeds the user's question and retrieves the top-K most semantically similar chunks
- Injects retrieved context into a grounded prompt (Week 3's "answer only from context" pattern, reused) and generates an answer
- Displays retrieved chunks and their similarity scores alongside every answer, so the answer's source is never a black box

Supporting infrastructure:
- `embedding.py`, `vector_store.py`, `retrieval.py`, `assistant.py` — each handling one stage of the pipeline
- `tests/test_embedding.py` and `tests/test_retrieval.py` — including a direct test of the classic semantic-search example ("Where should staff apply for vacation?" correctly matching "request annual leave")
- A custom lavender-gradient chat interface with a document "persona" card and per-message source citations

---

## 📖 What I Learned

- **Embeddings turn meaning into math.** Two sentences with almost no shared words ("How do I reset my password?" / "I forgot my login credentials.") can be mathematically close in vector space — this is the entire reason semantic search works where keyword search fails.
- **Cosine similarity measures direction, not magnitude.** This matters specifically for text embeddings, where raw vector length can vary for reasons unrelated to meaning.
- **A vector database isn't just "a database that stores vectors."** Its real value is doing similarity search efficiently at scale — something that would require slow, manual comparison loops otherwise.
- **Retrieval quality has a hard ceiling effect on generation quality.** No amount of good prompting fixes a wrong answer caused by retrieving the wrong context — this reinforces Week 3's Day 17 lesson from the opposite direction.
- **A pipeline can produce a correct final answer while an internal metric is silently broken.** This week's biggest technical lesson (see below) — the LLM's answer was right even while the displayed similarity scores were meaningless, because retrieval still returned reasonably relevant chunks despite the underlying distance metric being wrong.
- **The same UI bug pattern can recur across projects.** The "empty box" CSS issue from Week 3's sidebar navigation reappeared this week in the chat interface's persona card — recognizing it as a *pattern* (Streamlit's HTML-fragment rendering) rather than a one-off bug made it faster to diagnose and fix properly with `st.container(border=True)`.

---

## 🐞 Real Challenges Faced

### 1. Wrong similarity metric (cosine vs. L2 distance)
ChromaDB defaults to L2 (Euclidean) distance, not cosine similarity, unless explicitly configured. This wasn't caught immediately — the assistant's answers were still correct, because retrieval was returning reasonably relevant chunks regardless. The bug only became visible when the UI displayed similarity scores that didn't make sense (near-zero or negative for what should have been strong matches, e.g., 0.005, -0.148, -0.273). **Fix:** explicitly set `metadata={"hnsw:space": "cosine"}` when creating the ChromaDB collection.

### 2. Recurring "empty box" UI bug
The custom chat interface's persona card showed a stray empty rounded box with none of its intended content (icon, document stats, button) inside it. Root cause: opening an HTML `<div>` in one `st.markdown()` call and expecting subsequent `st.markdown()`/`st.button()` calls to render nested inside it — Streamlit treats each call as a separate HTML fragment, so the browser auto-closes the unclosed div immediately, leaving it empty. This is the exact same class of bug encountered in Week 3's sidebar navigation. **Fix:** replaced manual div-wrapping with Streamlit's native `st.container(border=True)`, which creates real persistent nested DOM structure.

### 3. Footer position shifting with content length
The footer used normal document flow (`margin-top`), so it appeared high on the page before any chat history existed, and moved down as messages accumulated — inconsistent and unprofessional-looking. **Fix:** changed to `position: fixed; bottom: 0;` so it stays anchored to the viewport regardless of content length.

### 4. Designing a chat-style history without a real backend
Since ChromaDB here runs in-memory (resets each session) and there's no persistent database for conversations, "chat history" had to be implemented entirely in `st.session_state` — meaning it resets on every app restart. This is an accepted limitation for this week's learning project, noted as a Future Improvement (persisting the vector database and conversation history across sessions).

---

## 🏆 Achievements

- A complete, working RAG pipeline: embeddings → vector storage → semantic retrieval → grounded generation → source display
- A direct, testable demonstration that semantic search succeeds where Week 3's keyword matching would fail (the "vacation" / "annual leave" example)
- A real production-grade bug (wrong distance metric) caught and fixed through careful inspection of displayed output, not just "it gave an answer, so it must be fine"
- A distinctive, fully custom chat interface — not a Streamlit default theme, and not a copy of Week 2/3's design system
- Consistent documentation and engineering journal practice carried through from Weeks 1–3

---

## 🔭 Next Week Preview

Week 4 completes the semantic search and RAG foundation of Phase 1. Refer to the roadmap for the Week 5 repository name and topic list once finalized.

---

## 📂 Git Commit

```bash
git add .
git commit -m "docs: add week 4 summary"
git push
```
