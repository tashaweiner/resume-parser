import os
import psycopg2
from dotenv import load_dotenv
import json
from  models.candidate import Candidate  # ✅ Adjusted to absolute import
import re
load_dotenv()

def extract_owner(filename: str) -> str | None:
    match = re.search(r'\((\w{2})\)\.pdf$', filename)
    return match.group(1) if match else None

def insert_parsed_resume(filename: str, parsed_data: Candidate):
    """Insert a parsed Candidate into the resumes table in Postgres."""

    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()

    # Extract fields
    name = parsed_data.name
    email = parsed_data.email
    phone = parsed_data.phone
    location = parsed_data.location
    skills = parsed_data.skills or []
    embedding = parsed_data.embedding
    owner = extract_owner(filename)
    parsed_json = json.dumps(parsed_data.dict())

    # Insert into table
    cur.execute("""
        INSERT INTO resumes (filename, name, email, phone, skills, location, parsed_json, embedding, owner)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (filename) DO NOTHING;
    """, (
        filename,
        name,
        email,
        phone,
        skills,
        location,
        parsed_json,
        embedding,
        owner
    ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Inserted into DB: {filename}")
  