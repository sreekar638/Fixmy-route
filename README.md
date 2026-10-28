# FixRoute — Problem-Solving & Complaint-Routing Platform

> **"Tell us your problem. We'll tell you who can fix it."**

FixRoute is a complete, production-ready, responsive web application that helps people across India identify the right authority to contact for a problem and guides them through the process of getting it resolved.

- **Founder & Owner:** Sreekar
- **Target Market:** India
- **Core Technology Stack:** Python 3.12 (FastAPI), SQLAlchemy Relational ORM, SQLite / PostgreSQL, Modern Responsive HTML5/CSS3/ES6 JavaScript.

---

## 🌟 Key Product Features

1. **Smart Natural-Language Problem Search**
   - Natural language description matching (e.g., *"My bank transaction failed but money was deducted"*).
   - Rule-based & database-backed ranking with geographic jurisdiction filtering across Indian states.
   - Transparent explanations showing why an authority was chosen.
   - Resilient AI assistant with an automatic offline fallback when API keys are absent.

2. **Verified Route Resolution Guides**
   - Step-by-step resolution roadmap citing official turnaround times (TAT) and acts.
   - Direct links to official government and regulatory portals (RBI CMS, NCH, UGC e-Samadhan, CGRF, DoT).
   - Critical warnings for statutory deadlines and eligibility prerequisites.
   - Interactive progress checkboxes persisted across sessions.

3. **Tailored Evidence Checklist**
   - Tailored checklist of required proofs (bills, unboxing videos, UTR numbers, tickets).
   - Ability to add custom checklist items and track collection progress.

4. **Complaint Generator**
   - Instant drafting of professional, polite, and factual legal complaints.
   - Writing styles: **Formal / Standard**, **Concise & Direct**, and **Detailed Legal Notice**.
   - One-click copy to clipboard, `.txt` download, printable PDF view, and prefilled email (`mailto:`) links.

5. **Complaint Progress Tracker**
   - Central tracker for reference numbers, submission dates, and status updates.
   - Chronological timeline logging.
   - Transparent disclaimer clarifying personal administrative statuses vs. external live portal states.

6. **Citizen Dashboard & User Accounts**
   - Secure bcrypt password hashing and JWT token authentication.
   - Saved problem routes, saved complaint drafts, and search history.
   - Full privacy rights: 1-click search history wipe and complete account deletion flow.

7. **Source Verification & Admin Portal**
   - Protected role-based administration portal (`role: admin`).
   - Route verification lifecycle (`verified`, `unverified`, `outdated`, `disputed`).
   - Community correction and broken link review queue.
   - Administrative audit log feed.

---

## 🏗️ Project Architecture

```
fixmy route/
├── backend/
│   ├── app/
│   │   ├── config.py             # Settings, environment, brand tokens, and secrets
│   │   ├── database.py           # Database engine, SessionLocal, Base
│   │   ├── seed_data.py          # Initial Indian categories, authorities, and routes
│   │   ├── models/               # SQLAlchemy ORM models
│   │   │   ├── user.py           # User, AuditLog
│   │   │   ├── route.py          # Category, ProblemRoute, ResolutionStep, Evidence, Source
│   │   │   ├── complaint.py      # ComplaintRecord, ComplaintTimeline, ComplaintDraft
│   │   │   └── feedback.py       # RouteCorrection, UserFeedback
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── routers/              # API endpoints
│   │   │   ├── auth.py           # Authentication (/api/auth)
│   │   │   ├── search.py         # Search engine (/api/search)
│   │   │   ├── routes.py         # Routes & categories (/api/categories, /api/routes)
│   │   │   ├── complaints.py     # Tracking (/api/complaints)
│   │   │   ├── drafts.py         # Drafting tool (/api/complaint-drafts)
│   │   │   ├── feedback.py       # Feedback & corrections (/api/feedback, /api/corrections)
│   │   │   ├── admin.py          # Admin portal (/api/admin)
│   │   │   └── ai.py             # Problem clarification (/api/ai)
│   │   └── services/             # Core engines
│   │       ├── search_engine.py  # Natural-language ranking & jurisdiction scoring
│   │       ├── complaint_gen.py  # Structured complaint drafting engine
│   │       ├── auth_service.py   # JWT & bcrypt authentication
│   │       └── ai_service.py     # Resilient AI helper with offline fallback
│   └── tests/                    # Pytest automated test suite
├── frontend/                     # Modern responsive UI
│   ├── index.html                # Homepage & Hero search
│   ├── search.html               # Search results & comparison
│   ├── route-detail.html         # Step-by-step guide & evidence checklist
│   ├── complaint-generator.html  # Multi-style letter generator
│   ├── tracker.html              # Complaint progress tracker
│   ├── dashboard.html            # User account hub
│   ├── admin.html                # Protected administration portal
│   ├── about.html                # Story, founder Sreekar, and 8 principles
│   ├── help.html                 # FAQs and contact form
│   ├── privacy.html              # Privacy policy & data protection
│   ├── terms.html                # Terms of service & legal disclaimer
│   ├── css/                      # Brand tokens, layout, and component styling
│   └── js/                       # Fetch API client and state management
├── main.py                       # Application entry point
├── requirements.txt              # Production dependencies
├── .env.example                  # Environment template
└── README.md
```

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- **Python 3.10+** (Python 3.12 recommended)
- **Git**

### 2. Clone and Setup Environment
```powershell
# Navigate into the project folder
cd "fixmy route"

# Create a virtual environment (if not already created)
python -m venv venv

# Activate the virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux / macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize & Seed Database
```powershell
# Windows PowerShell:
$env:PYTHONPATH = "."
python -m backend.app.seed_data

# Linux / macOS:
# PYTHONPATH=. python -m backend.app.seed_data
```
*This creates the database tables and seeds the 10 core Indian categories, verified problem routes, evidence requirements, and the initial Administrator account.*

### 4. Run the Development Server
```powershell
# Run using Python:
python main.py
```
Or with Uvicorn:
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the Web Application
- **Frontend Web App:** Open [http://localhost:8000](http://localhost:8000)
- **Interactive API Documentation:** Open [http://localhost:8000/docs](http://localhost:8000/docs)
- **System Health Endpoint:** Open [http://localhost:8000/health](http://localhost:8000/health)

### 6. Default Admin Account
- **Email:** `admin@fixroute.in`
- **Password:** `AdminSecureFixRoute2026!`
*(Change this in `.env` before deploying to production)*

---

## 🧪 Running Automated Tests

FixRoute includes a comprehensive pytest suite covering authentication, natural-language search, ranking, evidence checklists, draft generation, complaint tracking, and administrative access control.

```powershell
# Run the test suite:
$env:PYTHONPATH = "."
.\venv\Scripts\python.exe -m pytest -v
```

All 13 core tests will execute and pass:
```
backend/tests/test_fixroute.py::test_health_check PASSED
backend/tests/test_fixroute.py::test_list_categories PASSED
backend/tests/test_fixroute.py::test_natural_language_search_electricity PASSED
backend/tests/test_fixroute.py::test_natural_language_search_banking PASSED
backend/tests/test_fixroute.py::test_route_detail_and_steps PASSED
backend/tests/test_fixroute.py::test_user_registration_and_login PASSED
backend/tests/test_fixroute.py::test_complaint_draft_generation PASSED
backend/tests/test_fixroute.py::test_complaint_tracking_flow PASSED
backend/tests/test_fixroute.py::test_admin_authorization_and_stats PASSED
backend/tests/test_fixroute.py::test_feedback_and_correction_submission PASSED
backend/tests/test_fixroute.py::test_ai_clarification_fallback PASSED
backend/tests/test_frontend.py::test_frontend_routes_served PASSED
backend/tests/test_frontend.py::test_static_assets_served PASSED
```

---

## 🌐 Production Deployment Guide

### Recommended Platform: Render / Railway / DigitalOcean

1. **Environment Variables:**
   Set the following variables in your hosting dashboard:
   - `APP_ENV=production`
   - `DEBUG=False`
   - `SECRET_KEY=<generate-a-secure-random-64-character-string>`
   - `DATABASE_URL=postgresql://user:password@hostname:5432/dbname`
   - `CORS_ORIGINS=https://fixroute.in,https://www.fixroute.in`
   - `AI_PROVIDER=none` *(or `gemini` with `GEMINI_API_KEY`)*

2. **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Command:**
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT
   ```

---

## 🔒 Security & Privacy Notice
- **No Plaintext Passwords:** All passwords hashed with industry-standard salted `bcrypt`.
- **JWT Protection:** Access tokens signed using `HS256` with strict expiration windows.
- **Role-Based Protection:** Administrative routes strictly validated on the backend.
- **SQL Injection Prevention:** 100% parameterized queries via SQLAlchemy ORM.
- **Zero Sensitive Data Storage:** FixRoute never collects or retains banking credentials or identity secrets.
