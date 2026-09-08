"""
prompts.py
Reused from Week 3: Context + Question prompt pattern (Day 17) and
grounding system prompt (Day 19) — same pattern, now fed by semantic
retrieval instead of keyword matching or the full document.
"""

GROUNDED_SYSTEM_PROMPT = (
    "You are a knowledge assistant. Answer only from the provided "
    "context. If the answer is not present in the context, respond "
    "exactly with: 'I could not find this information in the provided "
    "document.' Do not use outside knowledge, and do not guess."
)


def build_qa_prompt(context: str, question: str) -> str:
    """Context + Question prompt pattern (Week 3, Day 17)."""
    return f"""Context:
{context}

Question:
{question}

Answer the question using only the information in the context above."""