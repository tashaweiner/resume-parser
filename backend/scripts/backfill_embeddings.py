import os
import psycopg2
from dotenv import load_dotenv
from models.candidate import Candidate
from utils.embeddings import get_embedding
from parser.flatten_candidate_for_embedding import flatten_candidate_for_embedding
import json

load_dotenv()

def generate_missing_embeddings():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()

    # Step 1: Fetch resumes missing embeddings
    cur.execute("SELECT filename, parsed_json FROM resumes WHERE embedding IS NULL")
    rows = cur.fetchall()
    print(f"\U0001F4C2 Found {len(rows)} resumes missing embeddings")

    for filename, parsed_json in rows:
        try:
            candidate = Candidate(**parsed_json)
            text = flatten_candidate_for_embedding(candidate)
            embedding = get_embedding(text)

            # Step 2: Update embedding
            cur.execute(
                "UPDATE resumes SET embedding = %s WHERE filename = %s",
                (embedding, filename)
            )
            print(f"✅ Embedded: {filename}")

        except Exception as e:
            print(f"❌ Failed for {filename}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    print("🚀 Done embedding all missing resumes.")

if __name__ == "__main__":
    generate_missing_embeddings()
