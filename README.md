# Personal RAG Assistant — Anshul Dhoot

A web chat interface where recruiters can ask questions about me instead of a standard screening call. Powered by LangChain, ChromaDB, and Streamlit.

## How It Works

```
knowledge_base/*.md  →  ingest.py  →  ChromaDB  →  retriever.py  →  chat.py  →  app.py (Streamlit)
```

1. KB documents (markdown files) are embedded and stored in ChromaDB
2. Recruiter asks a question via the Streamlit UI
3. Relevant chunks are retrieved and passed to GPT with a grounding prompt
4. Answer is returned in first-person, grounded in the KB
5. Visitor questions are logged to `logs/visitors.csv`
6. Scheduling intent triggers a Calendly link automatically

## Project Structure

```
personal-rag-assistant/
├── app.py                  # Streamlit UI — entry point
├── requirements.txt
├── .env.example            # Copy to .env and fill in keys
├── knowledge_base/         # Your KB markdown files go here
│   ├── kb_01_intro.md
│   ├── kb_02_experience.md
│   └── ...
├── chroma_db/              # Auto-created by ingest.py (gitignored)
├── logs/                   # Visitor log CSV (gitignored)
├── src/
│   ├── ingest.py           # Build the vector store from KB docs
│   ├── retriever.py        # Load ChromaDB and return retriever
│   ├── chat.py             # RAG chain + Calendly trigger logic
│   └── logger.py           # Visitor question logging
└── tests/
    └── test_retriever.py
```

## Setup

```bash
# 1. Clone and enter the project
git clone https://github.com/anshul-dhoot/personal-rag-assistant
cd personal-rag-assistant

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env — add your OPENAI_API_KEY and CALENDLY_URL

# 5. Copy KB docs into knowledge_base/
cp /path/to/kb_*.md knowledge_base/

# 6. Build the vector store
python -m src.ingest

# 7. Run the app
streamlit run app.py
```

## Re-ingesting After KB Updates

Whenever you add or edit KB documents, re-run ingestion:

```bash
python -m src.ingest
```

This rebuilds the ChromaDB collection from scratch.

## Visitor Logs

Questions are logged to `logs/visitors.csv` with session ID, timestamp, question, and answer snippet. Useful for understanding what recruiters are asking most.

## Related Project

[RAG Incident Assistant](https://github.com/anshul-dhoot/rag-incident-assistant) — production RAG pipeline for incident runbook retrieval.
