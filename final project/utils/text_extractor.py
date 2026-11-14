import os
from pypdf import PdfReader
from pptx import Presentation

def extract_text(file_path):
    """
    Extracts text from a PDF or PPTX file.
    Args:
        file_path (str): The path to the file.
    Returns:
        str: The extracted text.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.pptx':
        return extract_text_from_pptx(file_path)
    else:
        raise ValueError("Unsupported file format")

def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_pptx(file_path):
    text = ""
    try:
        prs = Presentation(file_path)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
    except Exception as e:
        print(f"Error reading PPTX: {e}")
    return text
