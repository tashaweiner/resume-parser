import os
import psycopg2
import re
from dotenv import load_dotenv

load_dotenv()

def extract_owner_from_filename(filename):
    match = re.search(r'\((\w{2})\)\.pdf$', filename)
    return match.group(1) if match else None

def backfill_owners():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()

    cur.execute("SELECT filename FROM resumes")
    rows = cur.fetchall()

    updated = 0
    for (filename,) in rows:
        owner = extract_owner_from_filename(filename)
        if owner:
            cur.execute(
                "UPDATE resumes SET owner = %s WHERE filename = %s",
                (owner, filename)
            )
            updated += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Backfilled owner for {updated} resumes.")

if __name__ == "__main__":
    backfill_owners()
