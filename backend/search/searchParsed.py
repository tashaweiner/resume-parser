import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from time import sleep

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
parsed_dir = "./output"

def load_resumes():
    all_resumes = []
    for file in os.listdir(parsed_dir):
        if file.endswith(".json"):
            with open(os.path.join(parsed_dir, file), "r") as f:
                data = json.load(f)
                all_resumes.append({"filename": file, "content": data})
    return all_resumes

def ask_gpt_to_score(batch, question):
    prompt = (
        f"You are reviewing candidate resumes in JSON format.\n"
        f"For each one, score how relevant it is to this question on a scale from 1 (not relevant) to 10 (perfect match).\n"
        f"Also give a short reason.\n\n"
        f"Question: {question}\n\n"
        f"Resumes:\n{json.dumps([r['content'] for r in batch], indent=2)}\n\n"
        f"Respond in this format:\n"
        f"Filename: <name>\nScore: <1-10>\nReason: <short text>\n---"
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
    for block in blocks:
        lines = block.strip().splitlines()
        data = {"filename": None, "score": 0, "reason": ""}
        for line in lines:
            if line.lower().startswith("filename"):
                data["filename"] = line.split(":")[1].strip()
            elif line.lower().startswith("score"):
                try:
                    data["score"] = int(line.split(":")[1].strip())
                except:
                    data["score"] = 0
            elif line.lower().startswith("reason"):
                data["reason"] = line.split(":", 1)[1].strip()
        if data["filename"]:
            candidates.append(data)
    return candidates

def search_and_rank(question):
    resumes = load_resumes()
    results = []

    for idx, batch in enumerate(batch_resumes(resumes)):
        raw = ask_gpt_to_score(batch, question)
        batch_scores = parse_gpt_response(raw)
        results.extend(batch_scores)
        sleep(1.5)  # avoid rate limit

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    return {
        "query": question,
        "results": sorted_results
    }

def print_ranked(results):
    print("\n🏆 Top Candidates by Relevance:\n")
    for i, r in enumerate(results):
        print(f"{i + 1}. {r['filename']} - Score: {r['score']} - {r['reason']}")

# --- CLI Usage Only ---
if __name__ == "__main__":
    print("🔍 AI Resume Ranking")
    query = input("What do you want to ask about the resumes?\n> ").strip()

    if query:
        final = search_and_rank(query)
        print_ranked(final["results"])
    else:
        print("⚠️ No question asked.")
