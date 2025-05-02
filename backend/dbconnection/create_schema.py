import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

schema_sql = """
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename TEXT UNIQUE NOT NULL,
    name TEXT,
    email TEXT,
    phone TEXT,
    skills TEXT[],
    location TEXT,
    parsed_json JSONB NOT NULL,
    parsed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT", 5432),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cur = conn.cursor()
cur.execute(schema_sql)
conn.commit()
cur.close()
conn.close()

print("✅ Table created (if it didn't already exist)")
