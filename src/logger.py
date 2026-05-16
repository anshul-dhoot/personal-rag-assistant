"""
logger.py
Logs visitor questions and metadata to a CSV file.
Each session gets a unique ID; questions are timestamped.
"""

import os
import csv
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

VISITOR_LOG_PATH = os.getenv("VISITOR_LOG_PATH", "./logs/visitors.csv")
FIELDNAMES = ["session_id", "timestamp", "question", "answer_snippet"]


def _ensure_log_file():
    """Create the log file with headers if it doesn't exist."""
    os.makedirs(os.path.dirname(VISITOR_LOG_PATH), exist_ok=True)
    if not os.path.exists(VISITOR_LOG_PATH):
        with open(VISITOR_LOG_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def generate_session_id() -> str:
    return str(uuid.uuid4())[:8]


def log_interaction(session_id: str, question: str, answer: str):
    """Append a single Q&A interaction to the visitor log."""
    _ensure_log_file()
    answer_snippet = answer[:120].replace("\n", " ") + "..." if len(answer) > 120 else answer
    row = {
        "session_id": session_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question.strip(),
        "answer_snippet": answer_snippet,
    }
    with open(VISITOR_LOG_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)
