"""
app.py
AI Knowledge Assistant — Streamlit UI
Developed by Hamna Munir

Chat-style interface inspired by a lavender-gradient assistant app:
left sidebar with question history, center chat bubbles (question/answer),
right-side "document persona" card, bottom pill-shaped composer.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.pdf_reader import extract_text_from_pdf, is_pdf_readable
from src.chunking import chunk_text
from src.vector_store import store_chunks, clear_collection
from src.assistant import answer_with_rag
from src.utils import format_preview, is_supported_file

st.set_page_config(page_title="AI Knowledge Assistant | Hamna Munir", page_icon="🧠", layout="wide")

# ---------------------------------------------------------------------------
# Custom CSS — lavender gradient chat theme
# ---------------------------------------------------------------------------

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp {
        background: linear-gradient(160deg, #5b4a7a 0%, #7a6291 35%, #9c86ab 70%, #c9b8cf 100%);
        color: #f3f0f7;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 1.6rem; max-width: 1200px; }
    [data-testid="stVerticalBlock"] { gap: 0.35rem !important; }
    .element-container { margin-bottom: 0 !important; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(30, 20, 45, 0.55);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    .brand { display: flex; align-items: center; gap: 0.5rem; font-weight: 800; font-size: 1.2rem; color: #fff; margin-bottom: 1.2rem; }
    .brand .dot { width: 10px; height: 10px; border-radius: 50%; background: #a78bfa; }

    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        background: #f3ead9;
        color: #4a3f5c;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 1rem;
        margin-bottom: 1rem;
    }

    .history-label { font-size: 0.72rem; color: rgba(255,255,255,0.55); letter-spacing: 1px; text-transform: uppercase; margin: 0.8rem 0 0.4rem 0.2rem; }
    .history-item {
        background: rgba(255,255,255,0.06);
        border-radius: 10px;
        padding: 0.55rem 0.8rem;
        margin-bottom: 0.4rem;
        font-size: 0.85rem;
        color: #e9e3f0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Chat area */
    .chat-title { font-size: 1.3rem; font-weight: 700; color: #fff; margin-bottom: 0.2rem; }
    .chat-subtitle { color: rgba(255,255,255,0.65); font-size: 0.88rem; margin-bottom: 1rem; }

    .bubble-row { display: flex; margin-bottom: 0.9rem; }
    .bubble-row.user { justify-content: flex-end; }
    .bubble-row.bot { justify-content: flex-start; }

    .bubble {
        max-width: 68%;
        padding: 0.9rem 1.15rem;
        border-radius: 16px;
        line-height: 1.55;
        font-size: 0.92rem;
    }
    .bubble.user {
        background: #f6efdf;
        color: #3d3350;
        border-bottom-right-radius: 4px;
    }
    .bubble.bot {
        background: rgba(40, 28, 58, 0.65);
        color: #f1ecf7;
        border: 1px solid rgba(255,255,255,0.08);
        border-bottom-left-radius: 4px;
    }
    .bubble-sources {
        margin-top: 0.6rem;
        padding-top: 0.6rem;
        border-top: 1px solid rgba(255,255,255,0.12);
        font-size: 0.76rem;
        color: rgba(255,255,255,0.55);
    }

    /* Right persona card — using Streamlit's native container(border=True)
       instead of a manually-opened div, which was creating a stray empty
       box (Streamlit closes unclosed HTML tags at the end of each
       markdown fragment, so a div opened in one st.markdown call and
       "closed" in a later call never actually nests real content). */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 18px !important;
        padding: 0.4rem;
    }
    .persona-icon {
        width: 76px; height: 76px; border-radius: 50%;
        background: linear-gradient(135deg, #a78bfa, #f0abfc);
        display: flex; align-items: center; justify-content: center;
        font-size: 2rem; margin: 0 auto 0.8rem auto;
    }
    .persona-name { font-weight: 700; color: #fff; font-size: 1.05rem; text-align: center; }
    .persona-role { color: rgba(255,255,255,0.6); font-size: 0.82rem; margin-bottom: 1rem; text-align: center; }
    .persona-stat { display: flex; justify-content: space-between; font-size: 0.8rem; color: rgba(255,255,255,0.75); padding: 0.35rem 0; border-top: 1px solid rgba(255,255,255,0.08); }
    .persona-stat b { color: #fff; }

    /* Uploader inside persona card */
    .stFileUploader section {
        background: rgba(255,255,255,0.06) !important;
        border: 1.5px dashed rgba(255,255,255,0.25) !important;
        border-radius: 12px !important;
    }
    .stFileUploader button {
        background: #a78bfa !important; color: white !important; border: none !important;
        border-radius: 8px !important; font-weight: 600 !important;
    }

    /* Composer */
    .composer-wrap {
        background: rgba(255,255,255,0.08);
        border-radius: 999px;
        padding: 0.4rem 0.5rem 0.4rem 1.2rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-top: 0.8rem;
    }
    .composer-wrap .stTextInput input {
        background: transparent !important;
        border: none !important;
        color: #fff !important;
        padding: 0.5rem 0 !important;
    }
    .composer-wrap .stTextInput input::placeholder { color: rgba(255,255,255,0.5); }
    .composer-wrap div[data-testid="column"] .stButton button {
        background: #2b1f3d;
        color: white;
        border-radius: 50%;
        width: 44px; height: 44px;
        padding: 0;
        font-size: 1.1rem;
    }

    .app-footer {
        position: fixed;
        bottom: 0; left: 0; right: 0;
        text-align: center;
        color: rgba(255,255,255,0.55);
        font-size: 0.78rem;
        padding: 0.6rem 0;
        background: rgba(30, 20, 45, 0.55);
        backdrop-filter: blur(6px);
        z-index: 100;
    }
    .app-footer b { color: #f0abfc; }
    .block-container { padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "indexed_doc" not in st.session_state:
    st.session_state.indexed_doc = None

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown('<div class="brand"><span class="dot"></span> Knowledge<b>AI</b></div>', unsafe_allow_html=True)

    if st.button("＋ New Conversation"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown('<div class="history-label">Recent Questions</div>', unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.markdown('<div class="history-item">No questions yet</div>', unsafe_allow_html=True)
    else:
        for entry in reversed(st.session_state.chat_history[-8:]):
            st.markdown(f'<div class="history-item">💬 {entry["question"]}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Main layout: chat (left/center) + persona card (right)
# ---------------------------------------------------------------------------

col_chat, col_persona = st.columns([2.3, 1])

with col_persona:
    with st.container(border=True):
        st.markdown("""
        <div class="persona-icon">🧠</div>
        <div class="persona-name">Knowledge Assistant</div>
        <div class="persona-role">Semantic Document Search</div>
        """, unsafe_allow_html=True)

        uploaded_file = None

        if st.session_state.indexed_doc is None:
            uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"], label_visibility="collapsed")

            if uploaded_file is not None:
                if not is_supported_file(uploaded_file.name):
                    st.error("Unsupported file type.")
                    st.stop()

                with st.spinner("Indexing..."):
                    full_text, total_pages = extract_text_from_pdf(uploaded_file)
                    if not is_pdf_readable(full_text):
                        st.warning("Couldn't extract text — may be scanned.")
                        st.stop()
                    clear_collection()
                    chunks = chunk_text(full_text, chunk_size=1000, overlap=100)
                    store_chunks(chunks, document_name=uploaded_file.name)
                    st.session_state.indexed_doc = uploaded_file.name
                    st.session_state.total_pages = total_pages
                    st.session_state.num_chunks = len(chunks)
                    st.rerun()
        else:
            uploaded_file = True

            st.markdown(f"""
            <div class="persona-stat"><span>Document</span><b>{st.session_state.indexed_doc}</b></div>
            <div class="persona-stat"><span>Pages</span><b>{st.session_state.total_pages}</b></div>
            <div class="persona-stat"><span>Chunks indexed</span><b>{st.session_state.num_chunks}</b></div>
            """, unsafe_allow_html=True)

            st.write("")
            if st.button("🔄 New Document"):
                clear_collection()
                st.session_state.indexed_doc = None
                st.session_state.chat_history = []
                st.rerun()

with col_chat:
    st.markdown('<div class="chat-title">Ask your document</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-subtitle">Search by meaning, not keywords — grounded answers powered by semantic retrieval.</div>', unsafe_allow_html=True)

    # Render chat history as bubbles
    for entry in st.session_state.chat_history:
        st.markdown(f'<div class="bubble-row user"><div class="bubble user">{entry["question"]}</div></div>', unsafe_allow_html=True)

        sources_html = ""
        if entry.get("sources"):
            src_items = "".join(
                f'<div style="margin-top:0.4rem;"><b>Chunk #{s["metadata"]["chunk_index"]}</b> '
                f'(sim {s["similarity"]:.2f}) — {format_preview(s["text"], max_chars=120)}</div>'
                for s in entry["sources"]
            )
            sources_html = f'<div class="bubble-sources">📎 Retrieved chunks:{src_items}</div>'

        st.markdown(f'<div class="bubble-row bot"><div class="bubble bot">{entry["answer"]}{sources_html}</div></div>', unsafe_allow_html=True)

    if st.session_state.indexed_doc is None:
        st.markdown('<div class="bubble-row bot"><div class="bubble bot">👋 Upload a document on the right to get started, then ask me anything about it.</div></div>', unsafe_allow_html=True)

    # Composer
    st.markdown('<div class="composer-wrap">', unsafe_allow_html=True)
    c1, c2 = st.columns([6, 1])
    with c1:
        question = st.text_input("msg", placeholder="Type a message...", label_visibility="collapsed", key="composer_input")
    with c2:
        send = st.button("➤", key="send_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    if send and question.strip() and st.session_state.indexed_doc is not None:
        with st.spinner("Searching by meaning..."):
            result = answer_with_rag(question, top_k=3)
        st.session_state.chat_history.append({
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"],
        })
        st.rerun()

st.markdown("""
<div class="app-footer">
    AI Knowledge Assistant · Week 4 of a 90-Day AI Engineering Roadmap · Developed by <b>Hamna Munir</b>
</div>
""", unsafe_allow_html=True)