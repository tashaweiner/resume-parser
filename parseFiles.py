import os
import fitz  # PyMuPDF
import openai
import json
from dotenv import load_dotenv
from time import sleep

# Load OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define folders
pdf_dir = "./resumes"
output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

# Function to extract text from a PDF
def extract_text_from_pdf(filepath):
    with fitz.open(filepath) as doc:
        return "\n".join([page.get_text() for page in doc])

# Function to call OpenAI and convert resume to structured JSON
def convert_to_json(resume_text):
    prompt = (
        "Extract structured resume data from the following text and return valid JSON with fields:\n"
        "- name\n- phone\n- email\n- experience (list with title, company, location, dates, and responsibilities)\n"
        "- education (school, degree, field, dates)\n- certifications\n\n"
        f"Resume:\n{resume_text}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    output = response['choices'][0]['message']['content']
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        print("⚠️ Couldn't parse JSON. Saving raw response.")
        return output

# Main loop over PDFs
for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        print(f"📄 Processing {filename}")
        filepath = os.path.join(pdf_dir, filename)
        text = extract_text_from_pdf(filepath)
        structured_data = convert_to_json(text)

        output_filename = filename.replace(".pdf", ".json")
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            if isinstance(structured_data, dict):
                json.dump(structured_data, f, indent=2)
            else:
                f.write(structured_data)

        print(f"✅ Saved: {output_filename}")
        sleep(1.5)  # Optional: avoid hitting OpenAI rate limits
