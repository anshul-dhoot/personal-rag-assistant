# Personal RAG Assistant — Product Backlog

> This is a live document. Items move from backlog → in progress → done as the product evolves.
> Priority: P1 = must have, P2 = should have, P3 = nice to have

---

## ✅ Done

| Feature | Notes |
|---------|-------|
| RAG pipeline — LangChain + ChromaDB + OpenAI | Core Q&A working |
| 9 KB documents covering key recruiter questions | Intro, YOE, skills, location, notice, salary, why move, IC/EM, day-to-day |
| Streamlit UI — two column layout | Chat left, profile + suggestions right |
| Profile photo in sidebar | Proper headshot, circular crop |
| Suggested questions panel | 9 common recruiter questions |
| Visitor logging to CSV | Session ID, timestamp, question, answer snippet |
| Single end-of-session feedback | Rating + open text, logged to CSV |
| Hallucination guardrail | System prompt refuses out-of-KB answers, routes to email |
| Tone guardrail | No corporate fluff — conversational, first-person |
| Deployed on Streamlit Cloud | Public URL live |
| Resume updated with Interactive Profile link | Clickable link added to PDF header |
| GitHub repo published | Public engineering portfolio |

---

## 🔵 P1 — Next Up

### 1. Visitor Log Persistence (Critical)
**Problem:** CSV lives on Streamlit Cloud's ephemeral filesystem — resets on every reboot, losing all visitor and feedback data.
**Solution:** Replace CSV logging with Google Sheets via gspread. Free, persistent, accessible from phone.
**Effort:** Small — 1 session
**Why it matters:** Without this, you have no visibility into who's visiting or what they're asking.

### 2. Admin Dashboard
**Problem:** Currently have to pull GitHub repo and open CSV to see visitor data.
**Solution:** Separate `admin.py` Streamlit app in same repo, password-protected. Shows:
- Visitor sessions and question history
- Feedback ratings and comments
- Most frequently asked questions (helps prioritise new KB docs)
**Effort:** Medium — 1-2 sessions
**Depends on:** Visitor log persistence fix above

### 3. Calendly Integration
**Problem:** "Schedule a call" footer is commented out — no way for interested recruiters to book directly.
**Solution:** 
- Set up Calendly free account
- Add URL to `.env` / Streamlit secrets
- Uncomment footer in `app.py`
- Auto-trigger Calendly nudge when scheduling keywords detected (already coded, just needs real URL)
**Effort:** Tiny — 30 mins once Calendly is set up

---

## 🟡 P2 — Should Have

### 4. KB Expansion and Refinement
**Problem:** Current 9 docs cover basics but miss depth. Recruiters will ask things not in the KB.
**Items to add:**
- Leadership style and philosophy
- How I handle conflict / team challenges
- What I look for in a team / company
- Specific project deep-dives (Deutsche Bank platform story)
- What I'm NOT looking for (helps filter bad fits early)
- Career goals — 3 year view
**Effort:** Ongoing — add 1-2 docs per week based on feedback data

### 5. Conversation Memory
**Problem:** Each question is answered in isolation. If a recruiter asks a follow-up, context is lost.
**Solution:** Add LangChain ConversationBufferMemory to maintain context within a session.
**Effort:** Small — 1 session
**Impact:** Makes conversation feel much more natural

### 6. RAGAS Evaluation
**Problem:** No way to measure answer quality objectively.
**Solution:** Integrate RAGAS metrics — faithfulness, answer relevance, context precision — to score RAG pipeline quality as KB grows.
**Effort:** Medium
**Impact:** Ensures quality doesn't degrade as more docs are added

### 7. Mobile UI Optimisation
**Problem:** Two-column layout doesn't work well on mobile — suggestions panel gets squished.
**Solution:** Detect mobile viewport, switch to single column with suggestions in a collapsible expander.
**Effort:** Small

---

## 🟢 P3 — Nice to Have

### 8. Multi-language Support
Allow recruiter to ask in Hindi or other languages — useful for domestic recruiters.

### 9. Resume Download Button
Add a "Download Resume" button in the sidebar below the profile card — recruiters can grab it directly without asking.

### 10. Analytics Dashboard (Public-facing)
A lightweight stats panel showing: "X recruiters have visited · Y questions asked" — social proof that the tool is active.

### 11. Email Notification on Visit
When a recruiter visits and asks questions, trigger an email notification to you — so you know in real time someone is actively looking.
**Tooling:** SendGrid free tier or Gmail SMTP

### 12. Version History for KB Docs
Track when each KB document was last updated — helps during interviews to show product thinking and iterative improvement.

### 13. Automated KB Refresh Trigger
When a new `.md` file is added to `knowledge_base/` on GitHub, auto-trigger ingestion so the vector store updates without manual `python -m src.ingest`.

---

## 💡 Product Thinking Notes

These are observations worth discussing during interviews to demonstrate product thinking:

- **The cold start problem** — first request on cloud always slow; solution is pre-warming the chain at import time (done) but a proper fix is async warm-up on deploy
- **Ephemeral filesystem vs persistent storage** — a real product decision: keep it simple (CSV) or build for reliability (Sheets/DB); chose simplicity first, now hitting the wall
- **Hallucination risk in personal branding** — unique problem: a wrong answer doesn't just mislead, it misrepresents you to a potential employer; solved with strict grounding prompt
- **Recruiter UX vs candidate control** — tension between making it frictionless for recruiters and ensuring every answer reflects how you actually think and speak; ongoing calibration via feedback loop
- **RAG vs fine-tuning** — deliberate choice: RAG lets you update your "knowledge" instantly by editing markdown files; fine-tuning would require retraining for every update — wrong tradeoff for a personal, evolving profile
- **Build vs buy** — could have used an off-the-shelf chatbot builder; chose to build because the product itself is the portfolio signal

---

*Last updated: May 2026*
*Owner: Anshul Dhoot*
*Repo: github.com/anshul-dhoot/personal-rag-assistant*
