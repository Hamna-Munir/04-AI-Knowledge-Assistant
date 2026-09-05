# Day 27 — Knowledge Assistant Testing

**Objective:** Check whether semantic retrieval is actually useful in practice — not just running once and assuming it works.

---

## 📖 Theory

### Retrieval quality

Retrieval quality is whether the chunks the system actually retrieves are the ones that genuinely help answer the question. A pipeline can be technically working (no errors, chunks returned) while still having poor retrieval quality (the wrong chunks, every time).

### Precision and recall (basic concept)

Two ways of measuring retrieval quality, at a beginner level:

- **Precision** — of the chunks retrieved, how many were actually relevant? (Are we returning junk along with the good stuff?)
- **Recall** — of all the relevant chunks that exist in the document, how many did we actually retrieve? (Are we missing important information?)

A system can have high precision but low recall (returns only 1 relevant chunk when 3 existed), or high recall but low precision (returns 10 chunks to make sure it caught everything, most of them irrelevant).

### Relevant vs irrelevant chunks

A relevant chunk actually contains information needed to answer the question. An irrelevant chunk was retrieved (perhaps due to a high similarity score) but doesn't actually help — this can happen when text is superficially similar in phrasing but not in substance.

### Retrieval failure

Retrieval failure is when the system fails to find the actually-relevant chunk, even though it exists in the document — the question and the answer just weren't embedded close enough together for that specific pairing of question phrasing and chunk phrasing.

### Hallucination (recap)

As covered in Week 3, hallucination is the model generating an answer not supported by real source material. Poor retrieval increases hallucination risk indirectly: if the LLM is given the wrong context, it may either produce a wrong answer confidently, or (if grounding is working correctly, per Week 3 Day 19) correctly say it couldn't find the answer — even though the real answer does exist in the document, just not in the retrieved chunk.

---

## 📚 Reading

[Evaluating RAG systems — retrieval metrics overview](https://www.pinecone.io/learn/series/rag/rag-evaluation/) (conceptual reference)

---

## 💻 Testing

Test with **at least 15 questions**, split into 4 categories:

- **5 easy questions** — answer clearly and directly stated in the document
- **5 semantic questions** — answer is in the document, but phrased very differently than the question (like the classic example below)
- **3 questions not in the documents** — should trigger the grounding "I don't know" response (Week 3, Day 19)
- **2 difficult/ambiguous questions** — no single clear-cut answer, testing how the system handles uncertainty

**Classic semantic test example:**

PDF says:
> "Employees can request annual leave through the HR portal."

Question:
> "Where should staff apply for vacation?"

Keyword matching (Week 3) would likely fail here — no shared words. Semantic retrieval should correctly connect "staff" ↔ "employees," "apply for vacation" ↔ "request annual leave."

---

## 🛠 Mini Project

Create an evaluation table:

| Question | Expected Chunk | Retrieved Chunk | Correct? |
|---|---|---|---|
| Q1 | Page 2 | Page 2 | Yes |
| Q2 | Page 5 | Page 5 | Yes |
| ... | ... | ... | ... |

Fill this in with real results from running all 15+ questions against the actual system.

---

## 🧠 Quiz

1. What's the difference between precision and recall, in simple terms?
2. Can a retrieval system have high precision but low recall? Give an example of what that would look like.
3. Why might the AI correctly say "I don't know" even when the real answer technically exists somewhere in the document?
4. Why are semantic (differently-worded) test questions specifically important to include, beyond just easy questions?

*(Try answering from memory first, then check the theory section above.)*

---

## ⭐ Bonus

Calculate a simple **retrieval success rate**: (number of questions where the correct chunk was retrieved) ÷ (total questions tested).

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Wrong top-K | K too low misses relevant chunks; K too high dilutes context with irrelevant ones | Test a few different K values against the same question set and compare results |
| Poor chunks | Chunk boundaries split relevant information awkwardly (Week 3, Day 18) | Revisit chunk size/overlap settings |
| Missing metadata | Can't verify *which* page/chunk was retrieved without stored metadata | Confirm metadata (Day 24) is present and accurate for every stored chunk |
| Retrieval returning unrelated information | Embedding model isn't capturing the specific domain's semantics well, or the question is too vague | Try rephrasing the question more specifically, or note this as a known limitation for very short/generic embedding models |

---

## ✅ Checklist

- [ ] 15+ questions tested across all 4 categories
- [ ] Semantic (differently-worded) queries specifically tested
- [ ] Out-of-document questions tested (grounding check)
- [ ] Evaluation table filled in with real results
- [ ] Retrieval failures documented, not just successes
- [ ] Git commit made

---

## 📂 Git Commit

```bash
git add .
git commit -m "test: evaluate semantic retrieval"
git push
```

---

## 📝 Journal

*Add Day 27's learning and biggest takeaway to `journal.md`.*
