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

# @router.post("/search")
# def search_resumes(request: SearchRequest):
#     if not request.question.strip():
#         raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
#     try:
#         results = search_and_rank(request.question)
#         return {"results": results}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/search")
# def search(query: str = Query(...)):
#     results = search_and_rank(query)
#     return results

@router.get("/search")
def search(query: str = Query(...)):
    results = search_and_rank(query)
    top_100 = sorted(results, key=lambda x: int(x["score"]), reverse=True)[:100]
    return {"results": top_100}

# @router.get("/resumes")
# def get_all_resumes():
#     resumes = []
#     for filename in os.listdir(OUTPUT_DIR):
#         if filename.endswith(".json"):
#             path = os.path.join(OUTPUT_DIR, filename)
#             with open(path, "r") as f:
#                 data = json.load(f)
#                 resumes.append({"filename": filename, "content": data})
#     return resumes

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

# @router.post("/refresh")
# def refresh_resumes():
#     download_resumes()    # <-- first pull new PDFs
#     parse_resumes()
#     return {"message": "Resumes refreshed"}