"""
assistant.py
Day 26 — the full RAG pipeline: retrieve relevant chunks via semantic
search, inject them into a grounded prompt, and generate an answer.
"""

from openai import OpenAI
from src.config import GROQ_API_KEY, GROQ_BASE_URL, GROQ_MODEL
from src.prompts import GROUNDED_SYSTEM_PROMPT, build_qa_prompt
from src.retrieval import retrieve_relevant_chunks

client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)


def _call_llm(prompt: str, temperature: float = 0.2, max_tokens: int = 500) -> str:
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": GROUNDED_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def answer_with_rag(question: str, top_k: int = 3) -> dict:
    """
    Full RAG pipeline: Question -> Embedding -> Vector Search ->
    Relevant Chunks -> Prompt + Context -> LLM -> Answer + Sources.

    Args:
        question: the user's question.
        top_k: how many chunks to retrieve as context.

    Returns:
        A dict with 'answer' and 'sources' (list of retrieved chunk info).
    """
    retrieved = retrieve_relevant_chunks(question, top_k=top_k)

    if not retrieved:
        return {
            "answer": "No document has been uploaded and indexed yet.",
            "sources": [],
        }

    context = "\n\n".join(chunk["text"] for chunk in retrieved)
    prompt = build_qa_prompt(context, question)
    answer = _call_llm(prompt)

    return {"answer": answer, "sources": retrieved}