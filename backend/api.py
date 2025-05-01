# backend/api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from onedrive.download_resumes import download_resumes  # adjust import path if needed
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

@router.get("/search")
def search(query: str = Query(...)):
    results = search_and_rank(query)
    return results

@router.get("/resumes")
def get_all_resumes():
    resumes = []
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith(".json"):
            path = os.path.join(OUTPUT_DIR, filename)
            with open(path, "r") as f:
                data = json.load(f)
                resumes.append({"filename": filename, "content": data})
    return resumes

@router.post("/refresh")
def refresh_resumes():
    download_resumes()    # <-- first pull new PDFs
    parse_resumes()
    return {"message": "Resumes refreshed"}