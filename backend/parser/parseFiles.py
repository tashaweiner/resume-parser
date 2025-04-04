import os
import fitz
from openai import OpenAI
import json
from dotenv import load_dotenv
from time import sleep

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Folder setup
pdf_dir = "./resumes"
output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

# Extract text from a PDF
def extract_text_from_pdf(filepath):
    with fitz.open(filepath) as doc:
        return "\n".join([page.get_text() for page in doc])

# Convert resume text to structured JSON using OpenAI
def convert_to_json(resume_text):
    prompt = (
        "Extract structured resume data from the following text and return valid JSON with fields:\n"
        "- name\n- phone\n- email\n- experience (list with title, company, location, dates, and responsibilities)\n"
        "- education (school, degree, field, dates)\n- certifications\n\n"
        f"Resume:\n{resume_text}"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    output = response.choices[0].message.content
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        print("⚠️ Couldn't parse JSON. Saving raw response.")
        return output

# Main parsing function
def parse_resumes():
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            output_filename = filename.replace(".pdf", ".json")
            output_path = os.path.join(output_dir, output_filename)

            # ✅ Skip if already parsed
            if os.path.exists(output_path):
                print(f"⏩ Skipping {filename} (already parsed)")
                continue

            print(f"📄 Processing {filename}")
            filepath = os.path.join(pdf_dir, filename)
            text = extract_text_from_pdf(filepath)
            structured_data = convert_to_json(text)

            with open(output_path, "w", encoding="utf-8") as f:
                if isinstance(structured_data, dict):
                    json.dump(structured_data, f, indent=2)
                else:
                    f.write(structured_data)

            print(f"✅ Saved: {output_filename}")
            sleep(1.5)  # Optional: helps avoid hitting rate limits

if __name__ == "__main__":
    parse_resumes()
