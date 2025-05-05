import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def convert_text_to_structured_json(resume_text: str):
    """Uses OpenAI to convert resume text into structured JSON aligned with Candidate model."""
    prompt = (
        "Extract structured resume data from the following text and return valid JSON with these exact fields:\n"
        "- name (string)\n"
        "- phone (string)\n"
        "- email (string)\n"
        "- location (string)\n"
        "- skills (list of strings)\n"
        "- certifications (list of strings)\n"
        "- experience (list of objects with: title, company, location, dates, responsibilities)\n"
        "- education (list of objects with: school, degree, field, dates)\n\n"
        "If a field is missing, return an empty string or an empty list.\n"
        "Return only valid JSON. No explanations.\n\n"
        f"Resume:\n{resume_text}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ OpenAI response was not valid JSON.")
        print("Response content:", content)
        return {
            "error": "Invalid JSON returned by OpenAI",
            "raw_response": content
        }
