from .extract_text import extract_text_from_pdf_bytes
from .generate_json import convert_text_to_structured_json
from models.candidate import Candidate
from pydantic import ValidationError

def parse_resume_pdf_bytes(file_bytes: bytes):
    """
    Given a resume PDF in bytes, returns a Candidate object if successful,
    or a dict with error details if parsing/validation fails.
    
    Steps:
    1. Extract text from PDF
    2. Send to OpenAI for structured data
    3. Validate against Candidate model
    """
    try:
        # 1. Extract raw text from the PDF
        text = extract_text_from_pdf_bytes(file_bytes)

        # 2. Convert the text to structured data via OpenAI
        structured_data = convert_text_to_structured_json(text)

        # 3. Wrap into a Candidate object
        candidate = Candidate(**structured_data)
        return candidate

    except ValidationError as ve:
        print("❌ Candidate validation failed:", ve)
        return {
            "error": "Invalid candidate structure",
            "details": ve.errors()
        }

    except Exception as e:
        print("⚠️ Error parsing resume:", e)
        return {
            "error": "Failed to parse resume",
            "details": str(e)
        }
