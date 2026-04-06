# 🔧 AI Resume Builder — Backend

> FastAPI + CrewAI backend that powers the AI Resume Builder. 4 specialized agents collaborate to analyze resume templates, write content, review it, and generate a structured PDF.

---

## 🏗️ Architecture

```
POST /generate
        ↓
Template PDF → pdfplumber (text extraction)
        ↓
CrewAI Multi-Agent Pipeline
    ├── 🔍 Template Analyzer  → extracts sections & structure
    ├── ✍️  Resume Writer      → writes tailored resume content
    ├── 🔎 Resume Reviewer    → polishes & ATS-optimizes
    └── 🏗️  PDF Builder        → converts output to structured JSON
        ↓
ReportLab → generates PDF
        ↓
FileResponse → PDF returned to frontend ✅
```

---

## 🛠️ Tech Stack

| Tech | Purpose |
|------|---------|
| FastAPI | REST API framework |
| CrewAI | Multi-agent orchestration |
| Gemini 1.5 Flash | LLM via Google AI |
| pdfplumber | PDF text extraction |
| ReportLab | PDF generation |
| python-dotenv | Environment variable management |
| Railway | Cloud deployment |

---

## 📁 Project Structure

```
backend/
├── main.py           ← FastAPI app & /generate endpoint
├── agents.py         ← 4 CrewAI agent definitions
├── tasks.py          ← Task definitions for each agent
├── crew.py           ← Crew assembly & kickoff
├── pdf_generator.py  ← ReportLab PDF builder
├── requirements.txt  ← Python dependencies
├── Procfile          ← Railway start command
├── runtime.txt       ← Python version (3.11.9)
└── .env              ← (not committed — add your own)
```

---

## 🤖 Agents

| Agent | Role |
|-------|------|
| **Template Analyzer** | Reads extracted PDF text and identifies all sections, their order, and field structure |
| **Resume Writer** | Writes a complete resume using user info, strictly following the template's structure |
| **Resume Reviewer** | Improves content with strong action verbs, concise language, and ATS optimization |
| **PDF Builder** | Converts the polished resume into a clean JSON object for PDF generation |

---

## 🚀 Local Setup

### 1. Clone & navigate

```bash
git clone https://github.com/Nivadeka222/resume-builder-backend.git
cd resume-builder-backend
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your free Gemini API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 5. Run the server

```bash
uvicorn main:app --reload
```

API will be live at `http://localhost:8000`

---

## 📡 API Endpoints

### `GET /`
Health check — confirms the API is running.

**Response:**
```json
{
  "status": "Resume Builder API is running"
}
```

---

### `POST /generate`
Generates a resume PDF based on the uploaded template and user details.

**Request:** `multipart/form-data`

| Field | Type | Description |
|-------|------|-------------|
| `template` | File (PDF) | Resume template to match in style |
| `name` | string | Full name |
| `phone` | string | Phone number |
| `email` | string | Email address |
| `linkedin` | string | LinkedIn profile name |
| `github` | string | GitHub URL |
| `job_title` | string | Target job title |
| `skills` | string | Technical skills |
| `education` | string | Education history |
| `experience` | string | Work experience |
| `projects` | string | Projects |
| `certifications` | string | Certifications |

**Response:** PDF file download

---

## 🌐 Deployment on Railway

### 1. Push to GitHub

```bash
git add .
git commit -m "initial commit"
git push origin main
```

### 2. Connect to Railway

1. Go to [railway.app](https://railway.app) → New Project
2. Select **Deploy from GitHub repo**
3. Choose `resume-builder-backend`

### 3. Add Environment Variables

In Railway → your service → **Variables** tab:
```
GEMINI_API_KEY = your_gemini_api_key_here
```

### 4. Get your live URL

Railway → your service → **Settings** → **Networking** → **Generate Domain**

Your backend will be live at:
```
https://your-app.up.railway.app
```

---

## 📦 Requirements

```
fastapi
uvicorn
crewai[google-genai]
pdfplumber
reportlab
python-dotenv
python-multipart
```

---

## ⚙️ Configuration Files

**`runtime.txt`** — tells Railway which Python version to use:
```
python-3.11.9
```

**`Procfile`** — tells Railway how to start the server:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## ⚠️ Important Notes

- Never commit your `.env` file — add it to `.gitignore`
- Gemini 1.5 Flash is free tier friendly and fast
- Resume generation takes ~30–60 seconds (4 agents run sequentially)
- Railway free tier provides $5/month credit — sufficient for personal use
- `verbose=False` is set on all agents to avoid Railway log rate limits

---

## 👩‍💻 Author

**Niva Rani Deka**
- GitHub: [@Nivadeka222](https://github.com/Nivadeka222)
- LinkedIn: [Niva Rani Deka](https://linkedin.com/in/Niva-Rani-Deka)

---

⭐ If you found this useful, give it a star!
