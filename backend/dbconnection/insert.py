import os
import psycopg2
from dotenv import load_dotenv
import json
from ..models.candidate import Candidate  # ✅ Adjusted to absolute import

load_dotenv()

def insert_parsed_resume(filename: str, candidate_data: Candidate):
    """Insert a parsed Candidate into the resumes table in Postgres."""

    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()

    # Extract key fields
    name = candidate_data.name
    email = candidate_data.email
    phone = candidate_data.phone
    location = candidate_data.location
    skills = candidate_data.skills or []

    # Convert full Candidate object to JSON for storage
    parsed_json = json.dumps(candidate_data.dict())

    # Insert into table
    cur.execute("""
        INSERT INTO resumes (filename, name, email, phone, skills, location, parsed_json)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (filename) DO NOTHING;
    """, (
        filename,
        name,
        email,
        phone,
        skills,
        location,
        parsed_json
    ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Inserted into DB: {filename}")
