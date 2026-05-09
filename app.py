import streamlit as st
import json
from agents.resume_parser import parse_resume
from agents.jd_parser import parse_job_description
from agents.scoring_agent import calculate_candidate_score
from agents.override_agent import apply_override
from utils.security import sanitize_input
from utils.db import init_db, save_override
from utils.report_generator import generate_pdf_report

st.set_page_config(
    page_title="AI HR Resume Screener",
    layout="wide"
)

init_db()

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: gray;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .section-header {
        font-size: 28px;
        font-weight: 600;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">AI HR Resume Shortlisting Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Automated candidate screening, ranking, and evaluation</div>',
    unsafe_allow_html=True
)


def clean_json(text):
    cleaned = text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.replace("```json", "")

    if cleaned.endswith("```"):
        cleaned = cleaned.replace("```", "")

    return cleaned.strip()


st.markdown(
    '<div class="section-header">Job Description Input</div>',
    unsafe_allow_html=True
)

jd_input = st.text_area(
    "Paste Job Description",
    height=220
)

uploaded_files = st.file_uploader(
    "Upload Candidate Resumes (PDF / DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

jd_data = None

if jd_input:
    try:
        safe_jd = sanitize_input(jd_input)

        with st.spinner("Analyzing job description..."):
            jd_result = parse_job_description(safe_jd)

        jd_data = json.loads(clean_json(jd_result))

        st.markdown(
            '<div class="section-header">Parsed Job Requirements</div>',
            unsafe_allow_html=True
        )

        st.json(jd_data)

    except Exception:
        st.error("Failed to parse job description.")


if uploaded_files and jd_data:
    ranking_results = []
    detailed_results = []

    for file in uploaded_files:
        try:
            with st.spinner(f"Analyzing {file.name}..."):
                resume_result = parse_resume(file)

            resume_data = json.loads(clean_json(resume_result))

            score = calculate_candidate_score(resume_data, jd_data)

            ranking_results.append({
                "Name": resume_data["name"],
                "Score": score["total_score"],
                "Recommendation": score["recommendation"],
                "Matched Skills": ", ".join(score["matched_skills"])
            })

            detailed_results.append({
                "candidate": resume_data,
                "score": score
            })

        except Exception:
            st.error(f"Failed to process {file.name}")

    ranking_results = sorted(
        ranking_results,
        key=lambda x: x["Score"],
        reverse=True
    )

    for idx, candidate in enumerate(ranking_results, start=1):
        candidate["Rank"] = idx

    st.markdown(
        '<div class="section-header">Candidate Ranking</div>',
        unsafe_allow_html=True
    )

    st.dataframe(ranking_results, use_container_width=True)

    pdf_path = generate_pdf_report(ranking_results)

    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    st.download_button(
        label="Download Shortlist PDF Report",
        data=pdf_bytes,
        file_name="shortlist_report.pdf",
        mime="application/pdf"
    )

    st.markdown(
        '<div class="section-header">Detailed Candidate Evaluation</div>',
        unsafe_allow_html=True
    )

    for item in detailed_results:
        candidate = item["candidate"]
        score = item["score"]

        with st.expander(
            f"{candidate['name']} | Score: {score['total_score']}"
        ):

            st.write("### Candidate Profile")
            st.json(candidate)

            st.write("### Score Breakdown")
            st.json(score)

            st.write("### Evaluation Summary")

            for explanation in score["explanations"]:
                st.write(f"- {explanation}")

            st.write("### HR Override")

            new_score = st.number_input(
                f"HR Override Score for {candidate['name']}",
                min_value=0,
                max_value=100,
                value=int(score["total_score"]),
                key=f"score_{candidate['name']}"
            )

            reason = st.text_area(
                f"HR Override Reason for {candidate['name']}",
                key=f"reason_{candidate['name']}"
            )

            if st.button(
                f"Apply HR Override for {candidate['name']}",
                key=f"btn_{candidate['name']}"
            ):
                updated_score = apply_override(score, new_score, reason)

                save_override(
                    candidate["name"],
                    score["total_score"],
                    new_score,
                    reason
                )

                st.success("HR override applied successfully.")
                st.json(updated_score)