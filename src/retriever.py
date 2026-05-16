"""
retriever.py
Loads the persisted ChromaDB vector store and exposes
a retriever for use by the chat module.
"""

import os
import httpx
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = "personal_rag"


def get_retriever(k: int = 4):
    """
    Load the ChromaDB vector store and return a retriever.
    k = number of chunks to retrieve per query.
    """
    import httpx
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        http_client=httpx.Client(),
        http_async_client=httpx.AsyncClient(),
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
    return retriever