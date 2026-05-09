from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


def parse_job_description(jd_text):
    prompt = f"""
    Extract job requirements from this job description.

    Return ONLY valid JSON.

    Format:
    {{
        "job_title": "",
        "required_skills": [],
        "preferred_skills": [],
        "experience_required": 0,
        "education_required": ""
    }}

    Rules:
    - No explanation
    - No markdown
    - Only JSON

    Job Description:
    {jd_text}
    """

    response = llm.invoke(prompt)
    return response.content