from docx import Document


def extract_text_from_docx(file):
    """
    Extract text from DOCX resume
    """
    try:
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()

    except Exception as e:
        return f"Error reading DOCX: {str(e)}"