# backend/api.py
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
from fastapi import APIRouter, HTTPException
import psycopg2
from pydantic import BaseModel
from search.searchParsed import search_and_rank
from parser.parseFiles import parse_resumes  # adjust import path if needed
from fastapi import APIRouter, Query
import os
import json

router = APIRouter()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
class SearchRequest(BaseModel):
    question: str

@router.get("/search")
def search(query: str = Query(...)):
    results = search_and_rank(query)
    top_50 = sorted(results, key=lambda x: int(x["score"]), reverse=True)[:50]
    return {"results": top_50}

@router.get("/resumes")
def get_all_resumes():
    print("🔍 DB host:", os.getenv("POSTGRES_HOST"))

    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT id, filename, name, email, phone, skills, location, parsed_at
        FROM resumes
        ORDER BY parsed_at DESC
    """)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    resumes = [dict(zip(columns, row)) for row in rows]

    cur.close()
    conn.close()
    return {"resumes": resumes}