"""
app.py
Streamlit chat interface for Anshul's Personal RAG Assistant.
Recruiters can ask questions and get answers grounded in the KB.

Run with:
    streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv
import os

from src.chat import ask
from src.logger import generate_session_id, log_interaction

load_dotenv()

APP_TITLE = os.getenv("APP_TITLE", "Chat with Anshul")
CALENDLY_URL = os.getenv("CALENDLY_URL", "https://calendly.com/your-link-here")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="💬",
    layout="centered",
)

# ── Session state init ────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = generate_session_id()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header ────────────────────────────────────────────────────────────────────
st.title("💬 Chat with Anshul Dhoot")
st.caption(
    "Engineering Manager · Data Platform · AI/GenAI · 17 Years · VP Deutsche Bank"
)
st.markdown(
    "Ask me anything — experience, skills, location, availability, what I'm looking for. "
    "No screening call needed to get started."
)
st.divider()

# ── Suggested questions ───────────────────────────────────────────────────────
with st.expander("💡 Not sure where to start? Try one of these"):
    suggestions = [
        "Tell me about yourself",
        "What are your core technical skills?",
        "How many years of experience do you have?",
        "Are you open to relocating?",
        "What is your notice period?",
        "Are you open to IC roles or only EM?",
        "Why are you planning to move?",
        "What does your typical week look like?",
    ]
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        if cols[i % 2].button(suggestion, key=f"suggest_{i}"):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            with st.spinner("Thinking..."):
                answer = ask(suggestion)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            log_interaction(st.session_state.session_id, suggestion, answer)
            st.rerun()

# ── Chat history ──────────────────────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question about Anshul..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask(prompt)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    log_interaction(st.session_state.session_id, prompt, answer)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    f"📅 Ready to connect? [Schedule a call with Anshul]({CALENDLY_URL})",
    unsafe_allow_html=False,
)
