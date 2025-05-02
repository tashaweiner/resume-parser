import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def convert_text_to_structured_json(resume_text: str):
    """Uses OpenAI to convert resume text into structured JSON."""
    prompt = (
        "Extract structured resume data from the following text and return valid JSON with fields:\n"
        "- name\n- phone\n- email\n- experience (list with title, company, location, dates, and responsibilities)\n"
        "- education (school, degree, field, dates)\n- certifications\n\n"
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
        # If the response is not valid JSON, log the error and return the raw content
        print("⚠️ OpenAI response was not valid JSON.")
        print("Response content:", content)
        return content
