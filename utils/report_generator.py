from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_pdf_report(ranking_results):
    os.makedirs("data/outputs", exist_ok=True)

    file_path = "data/outputs/shortlist_report.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("AI HR Resume Shortlisting Report", styles["Title"])
    )

    content.append(Spacer(1, 20))

    for candidate in ranking_results:
        line = (
            f"Rank: {candidate['Rank']} | "
            f"Name: {candidate['Name']} | "
            f"Score: {candidate['Score']} | "
            f"Recommendation: {candidate['Recommendation']}"
        )

        content.append(Paragraph(line, styles["Normal"]))
        content.append(Spacer(1, 12))

    doc.build(content)

    return file_path