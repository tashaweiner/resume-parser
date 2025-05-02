import fitz  # PyMuPDF

def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    """Extracts text from PDF bytes using PyMuPDF."""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        return "\n".join([page.get_text() or "" for page in doc.pages()])
