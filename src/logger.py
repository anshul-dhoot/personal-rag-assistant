"""
logger.py
Two types of email notifications:
1. Per-question alert — sent immediately when any question is asked
2. Session summary — sent when visitor submits feedback

Required in .env / Streamlit secrets:
    GMAIL_SENDER=your.email@gmail.com
    GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
    GMAIL_RECIPIENT=your.email@gmail.com
"""

import os
import csv
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

VISITOR_LOG_PATH = os.getenv("VISITOR_LOG_PATH", "./logs/visitors.csv")
GMAIL_SENDER = os.getenv("GMAIL_SENDER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
GMAIL_RECIPIENT = os.getenv("GMAIL_RECIPIENT", "")

FIELDNAMES = ["session_id", "timestamp", "question", "answer_snippet"]


def _ensure_log_file():
    os.makedirs(os.path.dirname(VISITOR_LOG_PATH), exist_ok=True)
    if not os.path.exists(VISITOR_LOG_PATH):
        with open(VISITOR_LOG_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def generate_session_id() -> str:
    return str(uuid.uuid4())[:8]


def _send_email(subject: str, body: str):
    """Core email sending — used by all notification types."""
    if not all([GMAIL_SENDER, GMAIL_APP_PASSWORD, GMAIL_RECIPIENT]):
        print("Email credentials not configured — skipping")
        return
    try:
        msg = MIMEMultipart()
        msg["From"] = GMAIL_SENDER
        msg["To"] = GMAIL_RECIPIENT
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Email failed: {e}")


def log_interaction(session_id: str, question: str, answer: str):
    """
    Log interaction to CSV and send per-question email alert.
    Feedback rows ([SESSION FEEDBACK]) trigger summary email instead.
    """
    _ensure_log_file()

    answer_snippet = (
        answer[:120].replace("\n", " ") + "..."
        if len(answer) > 120 else answer
    )
    row = {
        "session_id": session_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question.strip(),
        "answer_snippet": answer_snippet,
    }
    with open(VISITOR_LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)

    # Per-question email — skip internal feedback rows
    if not question.startswith("[SESSION FEEDBACK]") and not question.startswith("[FEEDBACK"):
        now = datetime.now().strftime("%b %d, %I:%M %p")
        subject = f"RAG — Question asked [{now}]"
        body = f"""Someone is on your RAG Assistant.

Session: {session_id}
Time: {datetime.now().strftime("%b %d, %Y — %I:%M %p IST")}
Question: {question}

Answer given:
{answer_snippet}

---
personal-rag-assistant-6zivofchzgcvpvsddenfxn.streamlit.app
"""
        _send_email(subject, body)


def _get_session_questions(session_id: str) -> list:
    """Read all real questions for a session from the CSV."""
    if not os.path.exists(VISITOR_LOG_PATH):
        return []
    questions = []
    with open(VISITOR_LOG_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            q = row["question"]
            if (row["session_id"] == session_id
                    and not q.startswith("[FEEDBACK")
                    and not q.startswith("[SESSION")):
                questions.append(q)
    return questions


def send_session_email(session_id: str, feedback_rating: str = "", feedback_comment: str = ""):
    """Send full session summary when feedback is submitted."""
    questions = _get_session_questions(session_id)
    count = len(questions)
    now = datetime.now()

    questions_text = "\n".join(
        f"  {i+1}. {q}" for i, q in enumerate(questions)
    ) if questions else "  (no questions recorded)"

    feedback_section = f"\nFeedback: {feedback_rating}" if feedback_rating else "\nFeedback: Not submitted"
    if feedback_comment:
        feedback_section += f'\nComment: "{feedback_comment}"'

    subject = f"RAG Session Summary — {count} question{'s' if count != 1 else ''} — {now.strftime('%b %d, %I:%M %p')}"
    body = f"""Session complete — visitor submitted feedback.

Time: {now.strftime("%b %d, %Y — %I:%M %p IST")}
Questions asked ({count}):
{questions_text}
{feedback_section}

---
personal-rag-assistant-6zivofchzgcvpvsddenfxn.streamlit.app
"""
    _send_email(subject, body)
