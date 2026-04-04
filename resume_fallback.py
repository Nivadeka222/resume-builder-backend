"""Plain-text resume when the LLM is unavailable (e.g. OpenAI quota exceeded)."""


def _format_skills(skills: str) -> str:
    parts = [p.strip() for p in skills.replace(";", ",").split(",") if p.strip()]
    return "\n".join(f"• {p}" for p in parts) if parts else "• (add your skills)"


def build_resume_template(user_info: dict) -> str:
    name = user_info.get("name", "").strip() or "Your Name"
    title = user_info.get("job_title", "").strip() or "Professional"
    skills = user_info.get("skills", "").strip()
    experience = user_info.get("experience", "").strip()
    education = user_info.get("education", "").strip()

    if not experience or experience.lower() in ("none", "n/a", "na", "-"):
        exp_section = (
            "Seeking opportunities to apply technical skills in a professional environment.\n"
            "Open to internships, junior roles, and projects that build on coursework and self-directed learning."
        )
    else:
        exp_section = experience

    edu_section = education or "Education details to be added."

    return f"""{name}
{title}

SUMMARY
Motivated candidate targeting {title.lower()} roles. Strong foundation in {skills or "relevant technical areas"}. Eager to contribute, learn quickly, and deliver quality work in team settings.

SKILLS
{_format_skills(skills)}

EXPERIENCE
{exp_section}

EDUCATION
{edu_section}
"""

