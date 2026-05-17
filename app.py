"""
app.py
Streamlit chat interface for Anshul Dhoot - Personal RAG Assistant.
Two-column layout: chat left, profile + suggestions right.
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

APP_TITLE = os.getenv("APP_TITLE", "Chat with Anshul")
CALENDLY_URL = os.getenv("CALENDLY_URL", "https://calendly.com/your-link-here")

st.set_page_config(page_title=APP_TITLE, page_icon="💬", layout="wide")

from src.chat import ask
from src.logger import generate_session_id, log_interaction

PHOTO_B64 = "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"

if "session_id" not in st.session_state:
    st.session_state.session_id = generate_session_id()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None
if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = False

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    .profile-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.2rem 1rem;
        text-align: center;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    .profile-card img {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        object-fit: cover;
        object-position: center top;
        border: 3px solid #1f4e79;
        margin-bottom: 0.5rem;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .profile-name {
        font-size: 1rem;
        font-weight: 700;
        color: #1f4e79;
        margin: 0 0 0.15rem 0;
    }
    .suggestion-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
    }
    .chat-header h2 {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1f4e79;
        margin: 0;
    }
    .chat-header p {
        font-size: 0.85rem;
        color: #6c757d;
        margin: 0.2rem 0 0 0;
    }
    .feedback-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border: 1px solid #e9ecef;
        margin-top: 1.5rem;
    }
    .feedback-box p {
        font-size: 0.88rem;
        color: #495057;
        margin: 0 0 0.8rem 0;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

chat_col, side_col = st.columns([2.2, 1], gap="large")

# RIGHT: Profile + Suggestions
with side_col:
    st.markdown(f"""
    <div class="profile-card">
        <img src="data:image/jpeg;base64,{PHOTO_B64}" alt="Anshul Dhoot"/>
        <p class="profile-name">Anshul Dhoot</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="suggestion-label">Try asking</p>', unsafe_allow_html=True)

    suggestions = [
        "Tell me about yourself",
        "What are your core tech skills?",
        "How many years of experience?",
        "Are you open to relocating?",
        "What is your notice period?",
        "Open to IC or EM roles?",
        "Why are you planning to move?",
        "What does your week look like?",
        "What salary are you expecting?",
    ]
    for i, s in enumerate(suggestions):
        if st.button(s, key=f"s_{i}", use_container_width=True):
            st.session_state.pending_question = s

# LEFT: Chat
with chat_col:
    st.markdown("""
    <div class="chat-header">
        <h2>💬 Chat with Anshul Dhoot</h2>
        <p>Engineering Manager · Data Platform · AI/GenAI · 17 Years · VP Deutsche Bank · Pune</p>
        <p style="margin-top:0.3rem; color:#495057;">
            Ask me anything — experience, skills, location, availability, what I'm looking for.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # Process suggestion button click
    if st.session_state.pending_question:
        q = st.session_state.pending_question
        st.session_state.pending_question = None
        st.session_state.messages.append({"role": "user", "content": q})
        with st.spinner("Thinking..."):
            ans = ask(q)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        log_interaction(st.session_state.session_id, q, ans)

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about Anshul..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ans = ask(prompt)
            st.markdown(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        log_interaction(st.session_state.session_id, prompt, ans)
        st.rerun()

    # Single end-of-session feedback — appears after first exchange
    if st.session_state.messages and not st.session_state.feedback_submitted:
        st.markdown("""
        <div class="feedback-box">
            <p>How did this go? Your inputs help improve the answers.</p>
        </div>
        """, unsafe_allow_html=True)

        rating = st.radio(
            "rating",
            ["Yes, got what I needed", "Not quite"],
            index=None,
            horizontal=True,
            label_visibility="collapsed",
            key="fb_rating"
        )
        fb_text = st.text_input(
            "fb_text",
            placeholder="Anything missing or unclear? (optional)",
            label_visibility="collapsed",
            key="fb_text_input"
        )
        if st.button("Submit feedback", key="fb_submit"):
            rating_val = rating or "no rating"
            fb_val = fb_text or "no comment"
            log_interaction(
                st.session_state.session_id,
                "[SESSION FEEDBACK]",
                f"{rating_val} | {fb_val}"
            )
            st.session_state.feedback_submitted = True
            st.success("Thanks — feedback noted!")
            st.rerun()

# Calendly footer — uncomment when URL is ready
# with chat_col:
#     st.divider()
#     st.markdown(f"[Schedule a call with Anshul]({CALENDLY_URL})")