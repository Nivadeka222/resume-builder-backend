from crewai import Task

def create_tasks(template_analyzer, writer, reviewer, pdf_builder, user_info, template_text):

    analyze_task = Task(
        description=f"""
        Analyze this resume template text and extract:
        1. All section names (e.g. Education, Experience, Projects, Skills, Certifications)
        2. The order of sections
        3. What fields each section contains (e.g. institution, degree, dates, bullets)
        4. The overall style (professional, creative, minimal, etc.)

        Template text:
        {template_text}

        Return a clear structured summary of the template layout.
        """,
        agent=template_analyzer,
        expected_output="A structured summary of all sections, their order, and fields in the template"
    )

    write_task = Task(
        description=f"""
        Using the template structure identified, write a complete resume for:

        Name: {user_info['name']}
        Phone: {user_info['phone']}
        Email: {user_info['email']}
        LinkedIn: {user_info['linkedin']}
        GitHub: {user_info['github']}
        Job Title: {user_info['job_title']}
        Skills: {user_info['skills']}
        Experience: {user_info['experience']}
        Projects: {user_info['projects']}
        Education: {user_info['education']}
        Certifications: {user_info['certifications']}

        Follow the EXACT same sections and order as the template.
        Write in plain text with clear section labels.
        """,
        agent=writer,
        expected_output="A complete resume in plain text following the template structure",
        context=[analyze_task]
    )

    review_task = Task(
        description="""
        Review the resume written by the Resume Writer.
        - Use strong action verbs
        - Make it ATS-friendly
        - Keep it concise and impactful
        - Do NOT change the section structure
        Return the final polished resume in plain text.
        """,
        agent=reviewer,
        expected_output="A polished, ATS-optimized resume in plain text",
        context=[write_task]
    )

    pdf_task = Task(
    description="""
    Convert the final resume into a JSON object for PDF generation.
    
    STRICT RULES:
    - Return ONLY the raw JSON object
    - No markdown, no backticks, no ```json, no extra text
    - No trailing commas anywhere
    - All keys and values must use double quotes
    - No single quotes anywhere
    - No comments inside JSON

    Use this exact structure:
    {
        "name": "Full Name",
        "phone": "+91 XXXXXXXXXX",
        "email": "email@example.com",
        "linkedin": "LinkedIn Name",
        "github": "github.com/handle",
        "education": [
            {
                "institution": "University Name",
                "location": "City, Country",
                "degree": "Degree Name",
                "dates": "Month Year - Month Year"
            }
        ],
        "experience": [
            {
                "company": "Company Name",
                "location": "Onsite",
                "role": "Role Title",
                "dates": "Month Year - Month Year",
                "bullets": ["Point 1", "Point 2"]
            }
        ],
        "projects": [
            {
                "name": "Project Name",
                "tech": "Tech Stack",
                "dates": "Month Year - Present",
                "bullets": ["Point 1", "Point 2"]
            }
        ],
        "skills": {
            "Category": "skill1, skill2"
        },
        "certifications": ["Cert 1", "Cert 2"]
    }
    """,
    agent=pdf_builder,
    expected_output="Valid raw JSON only, no markdown, no backticks, no extra text",
    context=[review_task]
)
    return [analyze_task, write_task, review_task, pdf_task]