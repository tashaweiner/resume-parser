import requests
from ..dbconnection.insert import insert_parsed_resume
from ..dbconnection.check_if_exists import is_resume_already_in_db
from .interactive_onedrive_auth import get_access_token
from ..parser.parse_resumes import parse_resume_pdf_bytes
from ..models.candidate import Candidate  # ✅ Import your Pydantic model

def download_and_parse_resumes():
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://graph.microsoft.com/v1.0/me/drive/root:/Resumes:/children"

    files = []
    while url:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        data = res.json()

        page_files = data.get("value", [])
        files.extend(page_files)
        url = data.get("@odata.nextLink")  # follow next page if exists

    print(f"📄 Found {len(files)} items in the Resumes folder")

    for file in files:
        filename = file["name"]

        if not filename.endswith(".pdf"):
            continue

        if is_resume_already_in_db(filename):
            print(f"⏭️ Already parsed: {filename}")
            continue

        print(f"⬇️ Downloading: {filename}")
        download_url = file["@microsoft.graph.downloadUrl"]
        file_bytes = requests.get(download_url).content

        parsed_candidate_data = parse_resume_pdf_bytes(file_bytes)

        if isinstance(parsed_candidate_data, Candidate):
            insert_parsed_resume(filename, parsed_candidate_data)
            print(f"✅ Inserted: {filename}")
        else:
            print(f"❌ Failed to parse: {filename}")
            print("Details:", parsed_candidate_data.get("details"))

if __name__ == "__main__":
    download_and_parse_resumes()
