# HireTrail AI 🧭
### *Your Personal AI Career Guidance Counselor*

HireTrail AI is a conversational AI career assistant that helps students and professionals navigate their career journey. It combines real-time web search, resume analysis, interview preparation, and personalized career advice — all through a single chat interface.
---
## 🚀 Live Demo
[**▶ Try HireTrail AI**](https://hiretrail-app.onrender.com/)

> ⚠️ Hosted on Render free tier — first load may take 30 seconds to wake up.

---
## Screenshots
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/717856c7-cf91-4cc2-bd4e-047f0d846a2f" />
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/9af1ebd0-61d3-40e2-bade-c230ee517db7" />
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/b084e34f-8743-4eab-8ce8-4c127a24299b" />
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/7aced1e3-019c-42b1-95d9-b7a3f42d4719" />
---

---
## ✨ Features

- **💬 Conversational Career Guidance** — Natural multi-turn conversations with full memory, focused exclusively on career topics
- **📄 Resume Analysis** — Upload your PDF resume and get personalized, specific feedback based on your actual experience
- **🔍 Real-Time Job Search** — Live job listings from Indeed, Naukri, LinkedIn and more — not training data
- **📚 Learning Resources** — Real courses, YouTube tutorials and certifications tailored to your goals
- **🎤 Interview Preparation** — Role-specific mock interviews, STAR method coaching and behavioral question practice
- **📊 Skill Gap Analysis** — Compare your current skills against market demand with actionable next steps
- **💼 LinkedIn & Portfolio Tips** — Profile optimization and portfolio building guidance

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | Chat UI and PDF upload |
| Backend | FastAPI | REST API server |
| LLM | Groq + LLaMA 3.3 70B | AI reasoning and responses |
| Search | Tavily API | Real-time web search |
| Resume Parsing | PyPDF2 | PDF text extraction |
| Security | python-dotenv | API key management |

---

## 🏗️ Architecture

```
User (Streamlit UI)
        ↓
POST /chat → FastAPI Backend
        ↓
Groq LLM (LLaMA 3.3 70B)
        ↓               ↓
  Needs search?      Direct reply
        ↓
  Tavily Search
  (live web data)
        ↓
  Groq → Final reply with links
        ↓
Streamlit displays response
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Groq API key → [console.groq.com](https://console.groq.com)
- Tavily API key → [tavily.com](https://tavily.com)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/shreyasvankhede/hiretrail-ai.git
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Running the App
Run on cloud-- https://hiretrail-app.onrender.com/

You need two terminals running simultaneously:

**Terminal 1 — Start FastAPI backend:**
```bash
uvicorn main:app --reload
```

**Terminal 2 — Start Streamlit frontend:**
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
hiretrail-ai/
├── main.py              ← FastAPI backend (LLM + search logic)
├── app.py               ← Streamlit frontend (UI + PDF upload)
├── .env                 ← API keys (never committed to GitHub)
├── .gitignore           ← ignores .env, venv, __pycache__
├── requirements.txt     ← all dependencies
├── logo.png             ← bot avatar
├── avatars/             ← random user avatars
│   ├── dog.png
│   ├── cat.png
│   ├── hamster.png
│   ├── panda.png
│   └── penguin.png
└── .streamlit/
    └── config.toml      ← Streamlit theme config
```

---

## 🔑 Key Technical Concepts

**Agentic Tool Calling**
Groq autonomously decides when to search the web based on the user's query. No hardcoded triggers — the LLM makes the decision using a two-call agentic loop.

**Dynamic Resume Context**
Resume text is injected into the system prompt at runtime when uploaded, making every response specific to the user's actual background and experience.

**Stateless LLM + Manual Memory**
Conversation history is managed client-side and filtered before each request, ensuring clean context without tool call internals leaking across turns.

**Malformed Tool Call Recovery**
A regex-based fallback recovers search queries even when Groq generates malformed tool calls, ensuring reliable search functionality.

**Prompt Engineering**
XML-structured system prompt with defined identity, strict boundaries, jailbreak protection, resume status verification, and explicit search behavior rules.

---

## 📦 Dependencies

```
fastapi
uvicorn
pydantic
groq
tavily-python
streamlit
requests
pypdf2
python-dotenv
```

Generate `requirements.txt`:
```bash
pip freeze > requirements.txt
```

---

## 🔒 Security

- API keys stored in `.env` file, never hardcoded
- `.env` added to `.gitignore` — never pushed to GitHub
- Resume text processed in memory, never stored permanently
- CORS middleware configured for development

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — Ultra-fast LLM inference
- [Tavily](https://tavily.com) — AI-optimized web search
- [FastAPI](https://fastapi.tiangolo.com) — Modern Python web framework
- [Streamlit](https://streamlit.io) — Rapid ML app development

---

*Built with ❤️ by Shreyas Vankhede*
