# Engineering Journal — Week 04

Daily engineering log for the AI Knowledge Assistant (Days 22–28). Not a personal diary — a record of what was built, what broke, and what would be done differently.

---

## Day 22

**Today**
Learned what embeddings actually are — text converted into a vector that captures meaning. Built `get_embedding()` using a local `sentence-transformers` model and tested the classic example: "How do I reset my password?" vs "I forgot my login credentials."

**Biggest Problem**
Understanding *why* two sentences with almost no shared words should be considered "similar" at all — this only clicked once actually comparing the raw vectors' cosine similarity and seeing the number confirm what intuition already suspected.

**How I Solved It**
Ran the password/credentials example directly and compared it against a genuinely unrelated sentence ("What's the weather like today?") — the contrast in similarity scores made the concept concrete instead of abstract.

**What I Would Improve**
Should test with more diverse sentence pairs (not just the one textbook example) to build real intuition for what similarity scores "feel like" a good match vs a weak one.

---

## Day 23

**Today**
Implemented `cosine_similarity()` from scratch and tested it against multiple sentences, confirming that semantically related sentences score higher than unrelated ones even without shared vocabulary.

**Biggest Problem**
Deciding whether to trust a manual cosine similarity implementation or rely on a library function — a subtle bug in a hand-written formula (e.g., forgetting to normalize) would silently produce wrong rankings without throwing any error.

**How I Solved It**
Wrote explicit unit tests for the manual implementation, including edge cases (identical vectors should score 1.0, orthogonal vectors should score 0.0) — these two checks alone would have caught a normalization bug immediately.

**What I Would Improve**
For anything beyond a learning exercise, I'd default to a well-tested library implementation (e.g., `sklearn.metrics.pairwise.cosine_similarity`) rather than a manual one, precisely because similarity bugs are easy to write and hard to notice just by eyeballing results.

---

## Day 24

**Today**
Set up ChromaDB, created a collection, and stored PDF chunks with embeddings and metadata (`document_name`, `chunk_index`).

**Biggest Problem**
Realized partway through that I hadn't specified which similarity metric ChromaDB should use for the collection — it defaults to L2 (Euclidean) distance, not cosine, which isn't obvious unless you go looking for it.

**How I Solved It**
This didn't fully surface as a problem until Day 26 testing (see below) — noted here because the root cause was introduced on this day, in `get_or_create_collection()`, by not passing `metadata={"hnsw:space": "cosine"}`.

**What I Would Improve**
Should have explicitly set the similarity metric on Day 24 itself, right when the collection was first created, instead of discovering the default was wrong only after seeing confusing output later.

---

## Day 25

**Today**
Built `retrieve_relevant_chunks()` — embeds the user's question and retrieves the top-K most similar stored chunks from ChromaDB, replacing Week 3's keyword-matching entirely.

**Biggest Problem**
Confirming retrieval was actually working correctly required a real semantic test, not just "did it return 3 results without erroring." The classic curriculum example — "Where should staff apply for vacation?" matching a chunk that says "request annual leave through the HR portal" — was the real test that mattered.

**How I Solved It**
Wrote `test_semantic_retrieval_finds_related_meaning_different_words()` specifically using that exact scenario, and confirmed the retrieved chunk did contain "annual leave" despite the question never using those words.

**What I Would Improve**
Should test retrieval against a wider variety of rephrasing styles (not just one canonical example) to get a better sense of how far the embedding model's semantic understanding actually stretches.

---

## Day 26

**Today**
Connected retrieval to the LLM, completing the full RAG pipeline (`answer_with_rag()`), and added source display so answers show which chunks they came from.

**Biggest Problem**
When testing the deployed pipeline end-to-end, the similarity scores shown in the UI were clearly wrong — near-zero or even negative values for what should have been strong, relevant matches (e.g., 0.005, -0.148, -0.273 for a correctly-answered question).

**How I Solved It**
Traced it back to Day 24's oversight: ChromaDB was using L2 distance by default, not cosine, so the `1 - distance` formula used to display "similarity" was meaningless — L2 distances aren't bounded the same way cosine distances are. Fixed by explicitly setting `metadata={"hnsw:space": "cosine"}` when creating the collection.

**What I Would Improve**
This is the clearest lesson of the week: a pipeline can produce a *correct final answer* while an internal metric (similarity score) is silently wrong — the LLM answered correctly regardless of the bad scores because retrieval still returned reasonably relevant chunks, which meant the bug was easy to miss unless someone actually looked at the displayed numbers critically instead of just checking "did I get an answer."

---

## Day 27

**Today**
Ran the assistant against a mix of easy, semantic, out-of-document, and ambiguous questions to evaluate real retrieval quality, following the same rigorous evaluation habit established in Week 2 (Day 13) and Week 3 (Day 20).

**Biggest Problem**
Deciding what "correct" means for an ambiguous question like "Is this a good place to work?" — there's no single right chunk to retrieve, so grading retrieval quality isn't as clean as it is for factual questions.

**How I Solved It**
Treated ambiguous questions as a separate category with a different success criterion: not "did it retrieve the exact right chunk," but "did it correctly recognize the question can't be answered from the document's factual content" — which is exactly what the grounding instruction is supposed to produce.

**What I Would Improve**
Should build out the full 15-question evaluation table with real results (as done for Week 2's Day 13 prompt evaluation) rather than treating this as a conceptual exercise — actual recorded results, including failures, are what make this evaluation genuinely useful going forward.

---

## Day 28

**Today**
Pulled the week together: fixed remaining UI issues (a persistent empty box caused by Streamlit's HTML fragment limitation — the same root cause as an issue from Week 3 — and a footer that moved position instead of staying fixed), reviewed the full pipeline end-to-end, and prepared for shipping.

**Biggest Problem**
The stray empty box in the custom chat UI came from opening an HTML `<div>` in one `st.markdown()` call and expecting later `st.markdown()`/`st.button()` calls to render inside it — Streamlit renders each call as a separate HTML fragment, so the browser auto-closes the unclosed `<div>` at the end of its own fragment, leaving an empty styled box with none of the intended content inside it.

**How I Solved It**
Replaced the manual div-wrapping approach with Streamlit's native `st.container(border=True)`, which creates real nested DOM structure that persists across multiple Streamlit calls inside the `with` block — solving the nesting problem at the framework level instead of fighting it with more CSS.

**What I Would Improve**
This is the second time this exact class of bug has appeared (first in Week 3's sidebar navigation, now here). Going forward, any time a "wrap several Streamlit calls in one styled container" need comes up, default to `st.container(border=True)` (or a single combined `st.markdown()` call for purely static content) instead of manually opening/closing divs across multiple calls.

---

## Week 04 — Overall Reflection

Two lessons stood out this week, and they rhyme with earlier weeks' lessons in a useful way. First: a pipeline can look like it's working (a correct final answer) while a component inside it is quietly broken (the cosine-vs-L2 distance bug) — exactly the kind of thing that only surfaces when you inspect intermediate outputs critically, not just the final result, echoing Week 2's Day 13 discovery that a "smarter-looking" prompt can still fail silently. Second: the empty-box CSS bug recurring from Week 3 is a reminder that recognizing a *pattern* of failure (Streamlit's fragment-based rendering) is more valuable long-term than fixing each instance of it individually.
