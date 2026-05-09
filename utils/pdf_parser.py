import fitz  

def extract_text_from_pdf(file):
    """
    Extract text from PDF resume
    """
    text = ""

    try:
        pdf = fitz.open(stream=file.read(), filetype="pdf")

        for page in pdf:
            text += page.get_text()

        pdf.close()
        return text.strip()

    except Exception as e:
        return f"Error reading PDF: {str(e)}"