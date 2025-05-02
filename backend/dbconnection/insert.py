import os
import psycopg2
from dotenv import load_dotenv
import json

load_dotenv()

def insert_parsed_resume(filename: str, parsed_data: dict):
    """Insert a parsed resume into the resumes table in Postgres."""

    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    cur = conn.cursor()

    # Extract basic fields from parsed_data safely
    name = parsed_data.get("name")
    email = parsed_data.get("email")
    phone = parsed_data.get("phone")
    location = parsed_data.get("location")
    skills = parsed_data.get("skills") or []

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
        json.dumps(parsed_data)
    ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Inserted into DB: {filename}")
