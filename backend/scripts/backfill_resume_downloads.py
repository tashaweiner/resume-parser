import os
import asyncio
import aiohttp
import asyncpg
from dotenv import load_dotenv
from ..onedrive.interactive_onedrive_auth import get_access_token
from ..parser.parse_resumes import parse_resume_pdf_bytes
from ..models.candidate import Candidate
from ..parser.flatten_candidate_for_embedding import flatten_candidate_for_embedding
from ..utils.embeddings import get_embedding
from ..dbconnection.insert import insert_parsed_resume

load_dotenv()

MAX_CONCURRENT = 5  # Limit to avoid hitting rate limits

async def is_resume_already_in_db_async(filename: str) -> bool:
    conn = await asyncpg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", 5432),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    row = await conn.fetchrow("SELECT 1 FROM resumes WHERE filename = $1", filename)
    await conn.close()
    return row is not None

async def fetch_resume_file(session, url):
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.read()

async def process_file(session, file):
    filename = file["name"]

    if not filename.endswith(".pdf"):
        return

    if await is_resume_already_in_db_async(filename):
        print(f"⏭️ Already parsed: {filename}")
        return

    print(f"⬇️ Downloading: {filename}")
    download_url = file["@microsoft.graph.downloadUrl"]
    file_bytes = await fetch_resume_file(session, download_url)

    parsed_candidate_data = parse_resume_pdf_bytes(file_bytes)

    if isinstance(parsed_candidate_data, Candidate):
        print(f"📝 Parsed: {filename}")

        flattened_text = flatten_candidate_for_embedding(parsed_candidate_data)
        parsed_candidate_data.embedding = get_embedding(flattened_text)

        insert_parsed_resume(filename, parsed_candidate_data)
        print(f"✅ Inserted into DB: {filename}")
    else:
        print(f"❌ Failed to parse: {filename}")
        print("Details:", parsed_candidate_data.get("details"))

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

        sem = asyncio.Semaphore(MAX_CONCURRENT)

        async def safe_process(file):
            async with sem:
                try:
                    await process_file(session, file)
                except Exception as e:
                    print(f"⚠️ Error processing {file['name']}: {e}")

        await asyncio.gather(*(safe_process(f) for f in files))

if __name__ == "__main__":
    asyncio.run(download_and_parse_all())
