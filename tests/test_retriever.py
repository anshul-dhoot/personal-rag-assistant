"""
test_retriever.py
Basic smoke tests for the retriever module.
Run with: pytest tests/
"""

import pytest
import os


def test_env_vars_present():
    """Ensure required env vars are set before running the app."""
    from dotenv import load_dotenv
    load_dotenv()
    assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not set in .env"
    assert os.getenv("CHROMA_PERSIST_DIR"), "CHROMA_PERSIST_DIR not set in .env"


def test_chroma_dir_exists():
    """ChromaDB directory should exist after ingestion."""
    from dotenv import load_dotenv
    load_dotenv()
    chroma_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    assert os.path.exists(chroma_dir), (
        f"ChromaDB dir not found at {chroma_dir}. Run: python -m src.ingest"
    )


def test_retriever_returns_results():
    """Retriever should return at least 1 result for a basic query."""
    from src.retriever import get_retriever
    retriever = get_retriever(k=2)
    results = retriever.invoke("years of experience")
    assert len(results) > 0, "Retriever returned no results"
