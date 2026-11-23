# AI CareerPilot 🚀
### Intelligent Multi-Agent AI Career Guidance & Employability Platform

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.1+](https://img.shields.io/badge/flask-3.1+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Google GenAI SDK](https://img.shields.io/badge/google--genai-3.6+-orange.svg)](https://pypi.org/project/google-genai/)
[![Test Suite](https://img.shields.io/badge/pytest-31%20passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

AI CareerPilot is a production-grade full-stack web application designed to help students, graduates, and professionals discover their optimal career paths, audit their resumes against ATS benchmarks, isolate critical skill gaps, follow personalized phased learning roadmaps, and excel in technical and behavioral interviews.

---

## 📑 Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Multi-Agent Architecture & Orchestration](#multi-agent-architecture--orchestration)
4. [Tech Stack](#tech-stack)
5. [Project Structure](#project-structure)
6. [Prerequisites](#prerequisites)
7. [Installation & Setup](#installation--setup)
8. [Configuring Google Gemini API Key](#configuring-google-gemini-api-key)
9. [Running the Application](#running-the-application)
10. [API Documentation](#api-documentation)
11. [Running Tests](#running-tests)
12. [Troubleshooting & FAQ](#troubleshooting--faq)
13. [Security & Privacy](#security--privacy)
14. [Future Enhancements](#future-enhancements)

---

## 🎯 Project Overview
Navigating tech careers in the era of artificial intelligence requires more than static advice. **AI CareerPilot** employs a coordinated multi-agent pipeline where six specialized agents collaborate to analyze a candidate's background, target career aspirations, and uploaded resume.

The platform provides:
- **Comprehensive Candidate Readiness Gauge**: Composite scoring taking into account foundational skills and ATS resume quality.
- **Calibrated Career Pathways**: Three realistic career roles ranked with match scores, current hiring demand, and salary benchmarks.
- **ATS Resume Auditor**: Identification of quantifiable strengths, weak phrasings, missing sections, and formatting optimizations.
- **Skill Gap Matrix**: Categorized competency deficits prioritized into High/Medium/Low urgency with time estimates.
- **Phased 4-Stage Learning Roadmap**: Structured milestones tailored to the candidate's exact daily study commitment.
- **Curated Capstone Projects**: Portfolio suggestions complete with tech stack tags and sample resume bullets.
- **Interview Preparation Coach**: Role-specific technical questions, STAR behavioral frameworks, and timed practice exercises.
- **Immediate Action Checklist**: Concrete tasks for immediate execution.

---

## ✨ Key Features
- **Futuristic SaaS Dark Interface**: Near-black background (`#05060b`), deep purple gradients, electric cyan (`#00f0ff`) and neon green (`#00ff9d`) accents, glassmorphic cards, and subtle glows.
- **Interactive Canvas Mesh**: Canvas with reactive mouse constellation lines, particle physics, and click-wave ripples (respects `prefers-reduced-motion`).
- **Drag-and-Drop Resume Ingestion**: Secure client-side parsing and verification for `.pdf`, `.txt`, and `.md` files up to 5MB.
- **Zero Data Retention**: Uploaded resumes are processed in-memory / temporary sandboxed files and purged immediately after analysis.
- **Graceful Offline Demo Mode**: If a Gemini API key is not configured or network quotas are exceeded, the platform automatically switches to an intelligent pre-trained heuristic fallback engine. The UI transparently indicates fallback status.
- **Report Export & Print**: One-click JSON export and formatted print layout for PDF generation.

---

## 🧠 Multi-Agent Architecture & Orchestration

### Honest Architectural Explanation
AI CareerPilot implements a **true modular multi-agent architecture** coordinated by a central `CareerOrchestrator`. Rather than packing the entire task into a single prompt, each agent is implemented in its own module with an isolated persona, system instruction, schema validation, and fallback handler.

```
                    ┌─────────────────────────┐
                    │     User Input &        │
                    │   Resume Ingestion      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Career Orchestrator   │
                    └────────────┬────────────┘
                                 │
      ┌──────────────────────────┴──────────────────────────┐
      │                                                     │
      ▼                                                     ▼
┌───────────────────────────┐                         ┌───────────────────────────┐
│ Agent 1: Profile Analysis │                         │ Agent 2: Resume Analyzer  │
│ Background, goals, habits │                         │ ATS audit, metrics, gaps  │
└─────────────┬─────────────┘                         └─────────────┬─────────────┘
              │                                                     │
              └──────────────────────────┬──────────────────────────┘
                                         ▼
                             ┌───────────────────────────┐
                             │ Agent 3: Career Pathing   │
                             │ Role matches & criteria   │
                             └───────────┬───────────────┘
                                         ▼
                             ┌───────────────────────────┐
                             │ Agent 4: Skill Gap Matrix │
                             │ Competencies & urgency    │
                             └───────────┬───────────────┘
                                         ▼
                             ┌───────────────────────────┐
                             │ Agent 5: Learning Roadmap │
                             │ Phased schedule & projects│
                             └───────────┬───────────────┘
                                         ▼
                             ┌───────────────────────────┐
                             │ Agent 6: Interview Prep   │
                             │ Tech, STAR & next steps   │
                             └───────────┬───────────────┘
                                         │
                                         ▼
                    ┌─────────────────────────┐
                    │ Unified Synthesis Report│
                    └─────────────────────────┘
```

### The 6 Specialist Agents:
1. **Profile Analysis Agent** (`agents/profile_agent.py`):
   - *Role*: Technical Career Strategist.
   - *Task*: Evaluates education, declared skills, experience level, career aspirations, and daily study hours.
2. **Resume Analyzer Agent** (`agents/resume_agent.py`):
   - *Role*: ATS Specialist & Technical Recruiter.
   - *Task*: Extracts text using `pypdf`, scores ATS alignment, flags weak passive phrasing, and highlights missing portfolio links or metrics.
3. **Career Path Agent** (`agents/career_path_agent.py`):
   - *Role*: Labor Market Analyst.
   - *Task*: Cross-references candidate strengths with market hiring data to recommend 3 calibrated roles with salary ranges and prerequisites.
4. **Skill Gap Agent** (`agents/skill_gap_agent.py`):
   - *Role*: Competency Lead & Skills Auditor.
   - *Task*: Compares candidate skills against role entry criteria, ranking gaps into High, Medium, or Low priority.
5. **Learning Roadmap Agent** (`agents/roadmap_agent.py`):
   - *Role*: Curriculum Architect & Mentor.
   - *Task*: Produces a 4-phase learning schedule aligned with available weekly hours and details 2 resume-ready capstone projects.
6. **Interview Preparation Agent** (`agents/interview_agent.py`):
   - *Role*: Bar Raiser & Technical Interview Coach.
   - *Task*: Generates 3 technical interview questions with grading criteria, 2 STAR behavioral questions, a practice exercise, and 5 actionable next steps.

---

## 💻 Tech Stack
- **Backend**: Python 3.11+, Flask 3.1, Werkzeug
- **AI Integration**: Official `google-genai` SDK (`from google import genai`)
- **Document Processing**: `pypdf 7.1+`
- **Environment & Secrets**: `python-dotenv`
- **Frontend**: Semantic HTML5, Responsive CSS3 (Flexbox/Grid), Vanilla JavaScript (ES6+)
- **Testing**: `pytest 9.2+`

---

## 📂 Project Structure
```
Aicoworker/
├── app.py                      # Flask Application entry point & API routes
├── config.py                   # Central configuration & environment bindings
├── requirements.txt            # Production dependencies
├── .env.example                # Template for environment variables
├── .env                        # Local environment configuration (git-ignored)
├── .gitignore                  # Git ignore rules for credentials & artifacts
├── README.md                   # Full documentation
├── agents/                     # Specialist AI Agents & Orchestrator
│   ├── __init__.py
│   ├── base_agent.py           # Abstract Base Agent with JSON extraction
│   ├── profile_agent.py        # 1. Profile Analysis Agent
│   ├── resume_agent.py         # 2. Resume Analyzer Agent
│   ├── career_path_agent.py    # 3. Career Path Agent
│   ├── skill_gap_agent.py      # 4. Skill Gap Agent
│   ├── roadmap_agent.py        # 5. Learning Roadmap Agent
│   ├── interview_agent.py      # 6. Interview Preparation Agent
│   └── orchestrator.py         # Multi-Agent Pipeline Coordinator
├── services/                   # Utility & Core Services
│   ├── __init__.py
│   ├── gemini_service.py       # Official Google GenAI SDK wrapper
│   ├── file_extractor.py       # PDF/TXT/MD extraction with automatic cleanup
│   ├── validator.py            # Input sanitization and validation
│   └── fallback_data.py        # Heuristic offline fallback data generator
├── public/                     # Frontend Assets (Vercel CDN, Flask locally)
│   ├── css/
│   │   └── style.css           # Futuristic dark SaaS styling
│   └── js/
│       ├── app.js              # Application logic, validation & rendering
│       └── canvas-bg.js        # Cyberpunk animated background & ripples
├── templates/
│   └── index.html              # Accessible semantic single-page UI
└── tests/                      # Automated Test Suite (31 Unit/Integration Tests)
    ├── __init__.py
    ├── test_health.py          # Health & index route tests
    ├── test_validation.py      # Field validation & sanitization tests
    ├── test_file_extractor.py  # PDF/TXT extraction & corruption tests
    ├── test_agents.py          # Individual agent & pipeline tests
    └── test_api.py             # Endpoint tests with mocked AI responses
```

---

## ⚙️ Prerequisites
- **Python 3.11 or higher** (Python 3.11, 3.12, 3.13, 3.14 supported)
- **pip** (Python package installer)
- *(Optional)* A free Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

---

## 📦 Installation & Setup

### 1. Clone or Open the Repository
```bash
cd Aicoworker
```

### 2. Create and Activate a Virtual Environment
#### On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

#### On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Configuring Google Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/) and sign in with your Google account.
2. Click **Get API key** and generate a new Gemini API Key.
3. Open the `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=AIzaSy...your_actual_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```
4. Save the file.

> **Note on Demo Mode:** If `GEMINI_API_KEY` is not provided or the network is offline, the application automatically runs in **Intelligent Demo / Fallback Mode**. You can test every feature immediately without an API key!

---

## 🚀 Running the Application

### Start the Flask Server:
#### On Windows (PowerShell):
```powershell
.\venv\Scripts\python.exe app.py
```

#### On macOS / Linux:
```bash
python3 app.py
```

### Access the Web Interface:
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📡 API Documentation

### 1. Health Status
- **Endpoint**: `GET /api/health`
- **Description**: Returns server status, uptime, and AI provider readiness.
- **Sample Response**:
  ```json
  {
    "status": "healthy",
    "service": "AI CareerPilot",
    "version": "1.0.0",
    "uptime_seconds": 12.4,
    "ai_integration": {
      "provider": "Google Gemini",
      "model": "gemini-2.5-flash",
      "api_key_configured": true,
      "mode": "Live Multi-Agent AI"
    },
    "timestamp": "2026-11-20T06:20:00.000000Z"
  }
  ```

### 2. Career Analysis
- **Endpoint**: `POST /api/analyze`
- **Content-Type**: `multipart/form-data` or `application/json`
- **Parameters**:
  - `name` *(string, optional)*: Candidate full name.
  - `education` *(string, required)*: Highest qualification or field.
  - `degree` *(string, optional)*: Specific major or degree title.
  - `year_of_study` *(string, optional)*: Study year or professional status.
  - `target_role` *(string, required)*: Career role targeted.
  - `experience_level` *(string, required)*: Entry-level, Student, Junior, Mid-level, Senior, Career Switcher.
  - `current_skills` *(string/list, required)*: Comma-separated or list of skills.
  - `hours_per_day` *(float/string, required)*: Available learning hours (0.5 to 16).
  - `interests` *(string, optional)*: Areas of technical interest.
  - `career_goals` *(string, optional)*: Professional career vision.
  - `resume` *(file, optional)*: Uploaded `.pdf`, `.txt`, or `.md` resume (up to 5MB).
- **Success Response Code**: `200 OK`
- **Error Response Codes**: `400 Bad Request` (validation error), `413 Payload Too Large`, `422 Unprocessable Entity` (corrupted file), `500 Internal Server Error`.

---

## 🧪 Running Tests
The project includes a 31-test suite with 100% pass rate covering unit logic, validation, file extraction, corruption recovery, mocked live AI calls, and fallback behaviors.

To run the test suite:
```powershell
.\venv\Scripts\pytest -v
```

---

## 🛠️ Troubleshooting & FAQ

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **"Script execution disabled" on Windows** | PowerShell execution policy restriction | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in your terminal. |
| **Banner shows "Demo Mode"** | `GEMINI_API_KEY` is not set in `.env` | Add your Gemini API key from AI Studio to `.env` and restart the server. |
| **"File size exceeds limit of 5MB"** | Uploaded resume is too large | Compress your resume or upload a plain text / markdown version. |
| **"Could not extract text from PDF"** | Scanned PDF containing image-only text | Export your resume as a text-readable PDF or copy-paste content into a `.txt` file. |

---

## 🔒 Security & Privacy
- **No Long-term File Storage**: Resumes are parsed in temporary memory and strictly unlinked/deleted immediately upon processing.
- **Zero Code Execution**: Uploaded files are strictly treated as inert text strings and sanitized against control characters and null bytes.
- **Key Safety**: The `GEMINI_API_KEY` is read only on the backend and is never exposed in client scripts, responses, or error traces.
- **XSS Prevention**: AI generated text is safely rendered using sanitized DOM manipulation, preventing script injection.

---

## 🔮 Future Enhancements
- Integration with live LinkedIn / GitHub job listings via webhooks.
- Audio-based mock technical interview practice with speech-to-text.
- Visual SVG dependency graphs for skill prerequisites.
- Export directly to Notion or Obsidian workspace.

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).
