"""
config.py
Loads environment variables (API keys, settings).
Configured for Groq (groq.com) — OpenAI-compatible API.
"""

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "openai/gpt-oss-120b"

# Embedding model — runs locally via sentence-transformers, no API key needed
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

if not GROQ_API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Did you add your Groq key to .env?")