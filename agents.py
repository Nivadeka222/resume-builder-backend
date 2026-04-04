from crewai import Agent
import os

def create_agents():
    llm = "gemini/gemini-2.5-flash"

    template_analyzer = Agent(
        role="Resume Template Analyzer",
        goal="Analyze the uploaded resume template and extract its structure, sections, and style details",
        backstory="You are an expert at reading and understanding resume layouts, identifying sections, formatting patterns, and design choices.",
        verbose=False ,
        allow_delegation=False,
        llm=llm
    )

    writer = Agent(
        role="Resume Writer",
        goal="Write a professional resume based on user info, following the exact structure extracted from the template",
        backstory="You are an expert resume writer who tailors content to match specific resume formats and structures.",
        verbose=False ,
        allow_delegation=False,
        llm=llm
    )

    reviewer = Agent(
        role="Resume Reviewer",
        goal="Review and improve the resume to be ATS-friendly, impactful, and polished",
        backstory="You are an HR expert who knows exactly what recruiters look for. You improve resumes with strong action verbs and clean formatting.",
        verbose=False ,
        allow_delegation=False,
        llm=llm
    )

    pdf_builder = Agent(
        role="PDF Structure Builder",
        goal="Convert the final resume content into a structured JSON that matches the template layout for PDF generation",
        backstory="You are a data formatting expert who converts resume text into clean structured JSON, preserving all sections and hierarchy.",
        verbose=False,
        allow_delegation=False,
        llm=llm
    )

    return template_analyzer, writer, reviewer, pdf_builder