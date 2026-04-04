from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pdfplumber
import json
import re
import os
import tempfile
from dotenv import load_dotenv
from crew import build_resume
from pdf_generator import generate_resume_pdf

load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Resume Builder API is running"}

@app.post("/generate")
async def generate(
    template: UploadFile = File(...),
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    linkedin: str = Form(...),
    github: str = Form(...),
    job_title: str = Form(...),
    skills: str = Form(...),
    education: str = Form(...),
    experience: str = Form(...),
    projects: str = Form(...),
    certifications: str = Form(...)
):
    # Read uploaded template PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await template.read())
        tmp_path = tmp.name

    template_text = ""
    with pdfplumber.open(tmp_path) as pdf:
        for page in pdf.pages:
            template_text += page.extract_text() or ""
    os.unlink(tmp_path)

    user_info = {
        "name": name, "phone": phone, "email": email,
        "linkedin": linkedin, "github": github,
        "job_title": job_title, "skills": skills,
        "education": education, "experience": experience,
        "projects": projects, "certifications": certifications
    }

    # Run CrewAI agents
    result = build_resume(user_info, template_text)

    # Extract JSON from result
    json_match = re.search(r'\{.*\}', result, re.DOTALL)
    if not json_match:
        return {"error": "Could not parse resume data from AI output"}

    resume_data = json.loads(json_match.group())

    # Generate PDF
    pdf_path = os.path.join(tempfile.gettempdir(), f"{name.replace(' ', '_')}_resume.pdf")
    generate_resume_pdf(resume_data, pdf_path)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{name.replace(' ', '_')}_resume.pdf"
    )