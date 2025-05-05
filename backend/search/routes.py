from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI, RateLimitError
import os
import psycopg2
import json
import re

from utils.embeddings import get_embedding
from parser.flatten_candidate_for_embedding import flatten_candidate_for_embedding
from models.candidate import Candidate

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SearchRequest(BaseModel):
    prompt: str
    top_k: int = 25
    owner: str | None = None  # 👈 add this line

@router.post("/semantic")
def semantic_search(request: SearchRequest):
    embedding = get_embedding(request.prompt)

    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()

    base_query = """
        SELECT filename, name, email, parsed_json, embedding <-> %s::vector AS distance
        FROM resumes
        WHERE embedding IS NOT NULL
    """
    params = [embedding]

    if request.owner:
        base_query += " AND owner = %s"
        params.append(request.owner)

    base_query += """
        ORDER BY embedding <-> %s::vector
        LIMIT %s;
    """
    params.extend([embedding, request.top_k])

    cur.execute(base_query, params)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "filename": row[0],
            "name": row[1],
            "email": row[2],
            "candidate": row[3],
            "distance": row[4]
        }
        for row in rows
    ]


@router.post("/gpt-score")
def gpt_score(request: SearchRequest, resumes: list[dict]):
    formatted_blocks = []

    for r in resumes:
        try:
            flat_text = flatten_candidate_for_embedding(Candidate(**r["candidate"]))
        except Exception:
            flat_text = json.dumps(r["candidate"])

        flat_text = flat_text[:1000]  # even tighter truncation to fit GPT-4 8k token limit
        formatted_blocks.append(
            f"Filename: {r['filename']}\nResume: {flat_text}\n"
        )

    # limit number of resumes to reduce token load
    formatted_blocks = formatted_blocks[:min(len(formatted_blocks), 10)]

    full_prompt = (
        f"You are an AI recruiter. Rank each resume for the following job description: '{request.prompt}'.\n"
        "Return a list in this format:\n"
        "Filename: <filename>\nScore: <1-10>\nReason: <short reason>\n\n"
        + "\n".join(formatted_blocks)
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.3,
        )
    except RateLimitError:
        raise HTTPException(status_code=429, detail="OpenAI rate limit exceeded or input too large.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OpenAI request failed: {str(e)}")

    raw = response.choices[0].message.content
    parsed = []
    for entry in raw.strip().split("Filename: ")[1:]:
        lines = entry.strip().split("\n")
        filename = lines[0].strip()
        score = int(re.search(r"\d+", lines[1]).group()) if len(lines) > 1 else None
        reason = lines[2].replace("Reason:", "").strip() if len(lines) > 2 else ""
        parsed.append({"filename": filename, "score": score, "reason": reason})

    return parsed

@router.post("/full")
def full_ranked_search(request: SearchRequest):
    semantic_results = semantic_search(request)
    top_for_gpt = semantic_results[:min(10, len(semantic_results))]  # GPT can only handle ~10 safely

    scored = gpt_score(request, top_for_gpt)

    # Map GPT scores by filename
    score_map = {entry["filename"]: entry for entry in scored}

    # Merge GPT scores into all semantic results
    for r in semantic_results:
        match = score_map.get(r["filename"])
        r["score"] = match["score"] if match else None
        r["reason"] = match["reason"] if match else None

    # Sort: scored first (high to low), unscored last
    semantic_results.sort(
        key=lambda r: (r["score"] is not None, r["score"] or 0),
        reverse=True
    )

    return {"results": semantic_results}
