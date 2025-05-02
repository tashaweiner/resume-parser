from dotenv import load_dotenv
load_dotenv()
import os
import json
from openai import OpenAI
from time import sleep
from dbconnection.load_resume_from_db import load_resume_from_db

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parsed_dir = os.path.join(BASE_DIR, "output")

def ask_gpt_to_score(batch, question):
    prompt = (
        "You are reviewing candidate resumes in JSON format.\n"
        "For each one, score how relevant it is to this question on a scale from 1 (not relevant) to 10 (perfect match).\n"
        "Also give a short reason. Respond with one block per resume in the following format:\n\n"
        "Filename: <name>\nScore: <1-10>\nReason: <short explanation>\n---\n"
        "If a resume is not relevant, still return it with Score: 1 and a short Reason.\n\n"
        f"Question: {question}\n\n"
        f"Resumes:\n{json.dumps([r['content'] for r in batch], indent=2)}"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

def batch_resumes(resumes, batch_size=10):
    for i in range(0, len(resumes), batch_size):
        yield resumes[i:i + batch_size]

def parse_gpt_response(response):
    candidates = []
    blocks = response.split("---")
    print(f"🧩 Found {len(blocks)} blocks in GPT response")

    for block in blocks:
        lines = block.strip().splitlines()
        data = {"filename": None, "score": 0, "reason": ""}

        for line in lines:
            if line.lower().startswith("filename"):
                data["filename"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("score"):
                try:
                    data["score"] = int(line.split(":", 1)[1].strip())
                except:
                    data["score"] = 0
            elif line.lower().startswith("reason"):
                data["reason"] = line.split(":", 1)[1].strip()

        if data["filename"]:
            candidates.append(data)

    return candidates

def search_and_rank(question):
    resumes = load_resume_from_db()
    results = []

    for idx, batch in enumerate(batch_resumes(resumes)):
        print(f"🔎 Processing batch {idx + 1} of {(len(resumes) + 9) // 10}")
        raw = ask_gpt_to_score(batch, question)
        print("🧠 Raw GPT response:\n", raw)
        batch_scores = parse_gpt_response(raw)
        results.extend(batch_scores)
        sleep(1.5)

    sorted_results = sorted(results, key=lambda x: int(x["score"]), reverse=True)
    return sorted_results  # ← ✅ FIXED: return the list directly
def print_ranked(results):
    print("\n🏆 Top Candidates by Relevance:\n")
    for i, r in enumerate(results):
        print(f"{i + 1}. {r['filename']} - Score: {r['score']} - {r['reason']}")

# CLI
if __name__ == "__main__":
    print("🔍 AI Resume Ranking")
    query = input("What do you want to ask about the resumes?\n> ").strip()

    if query:
        final = search_and_rank(query)
        if isinstance(final, dict) and "results" in final:
            print_ranked(final["results"])
        else:
            print("⚠️ GPT output was not in the expected format:", final)