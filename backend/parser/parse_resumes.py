from .extract_text import extract_text_from_pdf_bytes
from .generate_json import convert_text_to_structured_json

def parse_resume_pdf_bytes(file_bytes: bytes):
    """
    Given a resume PDF in bytes, returns structured resume data as JSON.
    Steps:
    1. Extract text from PDF
    2. Send to OpenAI
    3. Return structured resume data
    """
    text = extract_text_from_pdf_bytes(file_bytes)
    try:
        structured_data = convert_text_to_structured_json(text)
    except Exception as e:
        print("⚠️ Error parsing resume:", e)
        structured_data = {
            "error": "Failed to parse resume",
            "details": str(e)
        }
    return structured_data
