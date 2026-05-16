"""
ingest.py
Loads all markdown files from the knowledge_base/ directory,
splits them into chunks, embeds them, and stores in ChromaDB.

Run this once to build the vector store, and re-run whenever
you add or update KB documents.

Usage:
    python -m src.ingest
"""

import os
import glob
import httpx
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

KB_DIR = os.getenv("KB_DIR", "./knowledge_base")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = "personal_rag"


def load_documents():
    """Load all .md and .txt files from the knowledge base directory."""
    pattern = os.path.join(KB_DIR, "*.md")
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"No markdown files found in {KB_DIR}. Add your KB docs first.")
    
    docs = []
    for filepath in files:
        loader = TextLoader(filepath, encoding="utf-8")
        loaded = loader.load()
        # Tag each doc with its source filename for traceability
        for doc in loaded:
            doc.metadata["source"] = os.path.basename(filepath)
        docs.extend(loaded)
    
    print(f"Loaded {len(docs)} document(s) from {KB_DIR}")
    return docs


def split_documents(docs):
    """Split documents into chunks suitable for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=["\n\n", "\n", ".", " "],
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")
    return chunks


def build_vector_store(chunks):
    """Embed chunks and persist to ChromaDB."""
    import httpx
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        http_client=httpx.Client(),
        http_async_client=httpx.AsyncClient(),
    )

    # Wipe and rebuild — safe for a personal KB of this size
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PERSIST_DIR,
    )
    print(f"Vector store built and saved to {CHROMA_PERSIST_DIR}")
    return vector_store


def run():
    print("=== Starting KB Ingestion ===")
    docs = load_documents()
    chunks = split_documents(docs)
    build_vector_store(chunks)
    print("=== Ingestion Complete ===")


if __name__ == "__main__":
    run()
