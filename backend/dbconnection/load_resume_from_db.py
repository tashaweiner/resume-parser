from dotenv import load_dotenv

load_dotenv()
import psycopg2
import os


def load_resume_from_db():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()
    cur.execute("SELECT filename, name, email, phone, skills, location FROM resumes")
    rows = cur.fetchall()
    resumes = []

    for row in rows:
        filename, name, email, phone, skills, location = row
        resumes.append({
            "filename": filename,
            "content": {
                "name": name,
                "email": email,
                "phone": phone,
                "skills": skills,
                "location": location,
            }
        })

    cur.close()
    conn.close()
    return resumes
