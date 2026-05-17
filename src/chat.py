"""
chat.py
Core RAG chain. Takes a question, retrieves relevant KB chunks,
and generates a grounded answer using GPT.

Also handles Calendly trigger detection — if a recruiter asks
about scheduling or next steps, a Calendly prompt is returned.
"""

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from src.retriever import get_retriever

load_dotenv()

CALENDLY_URL = os.getenv("CALENDLY_URL", "https://calendly.com/your-link-here")

# Keywords that suggest the recruiter wants to schedule a call
CALENDLY_TRIGGERS = [
    "schedule", "call", "connect", "meet", "interview",
    "slot", "availability", "available", "book", "calendar",
    "talk", "speak", "discussion", "next steps",
]

SYSTEM_PROMPT = """You are representing Anshul Dhoot in conversation with recruiters.
Answer questions about Anshul using ONLY the context provided below.

STRICT RULES:
- If the answer is not in the context, respond exactly with: \
"I don't have that information here. You can reach Anshul directly at \
anshuldhoot.engineer@gmail.com to ask this."
- Never make up, infer, or assume anything not explicitly stated in the context
- No words like: passionate, expertise, excellence, thrive, seasoned, driven
- Write like a real person talking, not a LinkedIn profile
- Short, direct sentences. First person, conversational.
- Humble but confident — state facts, not superlatives

Context:
{context}

Question: {question}
Answer:"""

PROMPT = PromptTemplate(
    template=SYSTEM_PROMPT,
    input_variables=["context", "question"],
)


def should_show_calendly(question: str) -> bool:
    """Return True if the question contains scheduling intent."""
    q = question.lower()
    return any(trigger in q for trigger in CALENDLY_TRIGGERS)


def get_calendly_nudge() -> str:
    return (
        f"\n\n---\n📅 **Want to connect directly?** "
        f"[Schedule a call with Anshul]({CALENDLY_URL})"
    )


def build_chain():
    """Build and return the RetrievalQA chain."""
    retriever = get_retriever(k=4)
    import httpx
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        http_client=httpx.Client(),
        http_async_client=httpx.AsyncClient(),
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=False,
    )
    return chain


# Pre-warm the chain at import time so first request doesn't fail
try:
    _chain = build_chain()
except Exception as e:
    _chain = None
    print(f"Chain init failed: {e}")


def get_chain():
    global _chain
    if _chain is None:
        _chain = build_chain()
    return _chain


def ask(question: str) -> str:
    """
    Main entry point. Takes a question string, returns an answer string.
    Appends Calendly nudge if scheduling intent is detected.
    """
    chain = get_chain()
    result = chain.invoke({"query": question})
    answer = result.get("result", "").strip()

    if should_show_calendly(question):
        answer += get_calendly_nudge()

    return answer
