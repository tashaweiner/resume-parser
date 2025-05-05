import os
import asyncio
import aiohttp
import asyncpg
from dotenv import load_dotenv
from onedrive.interactive_onedrive_auth import get_access_token
from parser.parse_resumes import parse_resume_pdf_bytes
from models.candidate import Candidate
from parser.flatten_candidate_for_embedding import flatten_candidate_for_embedding
from utils.embeddings import get_embedding
from dbconnection.insert import insert_parsed_resume

load_dotenv()

MAX_CONCURRENT = 5

async def get_existing_filenames() -> set:
    conn = await asyncpg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", 5432),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    rows = await conn.fetch("SELECT filename FROM resumes")
    await conn.close()
    return set(row["filename"] for row in rows)

async def fetch_resume_file(session, url):
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.read()

async def process_file(session, file, existing_filenames: set):
    filename = file["name"]

    if not filename.endswith(".pdf"):
        return

    if filename in existing_filenames:
        print(f"⏭️ Already parsed: {filename}")
        return

    print(f"⬇️ Downloading: {filename}")
    download_url = file["@microsoft.graph.downloadUrl"]
    try:
        file_bytes = await fetch_resume_file(session, download_url)
        parsed_candidate_data = parse_resume_pdf_bytes(file_bytes)

        if not isinstance(parsed_candidate_data, Candidate):
            print(f"❌ Failed to parse: {filename}")
            print("Details:", parsed_candidate_data.get("details"))
            return

        print(f"📝 Parsed: {filename}")
        flattened_text = flatten_candidate_for_embedding(parsed_candidate_data)
        parsed_candidate_data.embedding = get_embedding(flattened_text)

        insert_parsed_resume(filename, parsed_candidate_data)
        existing_filenames.add(filename)  # update the set after success
        print(f"✅ Inserted into DB: {filename}")

    except Exception as e:
        print(f"⚠️ Error processing {filename}: {e}")

async def download_and_parse_all():
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://graph.microsoft.com/v1.0/me/drive/root:/Resumes:/children"

    files = []

    async with aiohttp.ClientSession(headers=headers) as session:
        while url:
            async with session.get(url) as resp:
                resp.raise_for_status()
                data = await resp.json()
                files.extend(data.get("value", []))
                url = data.get("@odata.nextLink")

        print(f"📁 Found {len(files)} items in the Resumes folder")

        existing_filenames = await get_existing_filenames()
        sem = asyncio.Semaphore(MAX_CONCURRENT)

        async def safe_process(file):
            async with sem:
                await process_file(session, file, existing_filenames)

        await asyncio.gather(*(safe_process(f) for f in files))

if __name__ == "__main__":
    asyncio.run(download_and_parse_all())
