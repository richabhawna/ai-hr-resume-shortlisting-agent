import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from utils.pdf_parser import extract_text_from_pdf
from utils.docx_parser import extract_text_from_docx
from utils.security import sanitize_input

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


def extract_resume_text(uploaded_file):
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    elif filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)

    return None


def parse_resume(uploaded_file):
    resume_text = extract_resume_text(uploaded_file)

    if not resume_text:
        return None

    resume_text = sanitize_input(resume_text)

    prompt = f"""
    Extract information from this resume.

    Return ONLY valid JSON.

    Format:
    {{
        "name": "",
        "email": "",
        "phone": "",
        "skills": [],
        "education": "",
        "experience_years": 0,
        "projects": []
    }}

    Rules:
    - No explanation
    - No markdown
    - Only JSON

    Resume:
    {resume_text}
    """

    response = llm.invoke(prompt)

    return response.content