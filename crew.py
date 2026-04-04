from crewai import Crew, Process
from agents import create_agents
from tasks import create_tasks

def build_resume(user_info, template_text):
    template_analyzer, writer, reviewer, pdf_builder = create_agents()
    tasks = create_tasks(template_analyzer, writer, reviewer, pdf_builder, user_info, template_text)

    crew = Crew(
        agents=[template_analyzer, writer, reviewer, pdf_builder],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    return str(result)