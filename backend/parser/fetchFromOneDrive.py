# backend/parser/fetch_from_onedrive.py
import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("ONEDRIVE_CLIENT_ID")
client_secret = os.getenv("ONEDRIVE_CLIENT_SECRET")
tenant_id = os.getenv("ONEDRIVE_TENANT_ID")
folder_id = os.getenv("ONEDRIVE_FOLDER_ID")  # Optional
drive_id = os.getenv("ONEDRIVE_DRIVE_ID")  # Optional
authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["https://graph.microsoft.com/.default"]

# app = ConfidentialClientApplication(
#     client_id,
#     authority=authority,
#     client_credential=client_secret
# )

# token = app.acquire_token_for_client(scopes=scope)
# print(token)
# access_token = token["access_token"]
# # print(access_token)

# headers = {
#     "Authorization": f"Bearer {access_token}"
# }

# # Fetch files in root or specific folder
# # this is temp just to query my practice Resume Folder 
# url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/Resumes:/children"

# print(url)
# res = requests.get(url, headers=headers)
# print(res)
# files = res.json().get("value", [])

# print(f"📄 Found {len(files)} items in the Resumes folder")

# # Download PDFs
# for file in files:
#     if file["name"].endswith(".pdf"):
#         download_url = file["@microsoft.graph.downloadUrl"]
#         content = requests.get(download_url).content
#         with open(f"backend/resumes/{file['name']}", "wb") as f:
#             f.write(content)
#             print(f"✅ Downloaded: {file['name']}")
from msal import PublicClientApplication, SerializableTokenCache

cache_path = os.path.expanduser("~/.msal_token_cache.bin")
token_cache = SerializableTokenCache()

if os.path.exists(cache_path):
    token_cache.deserialize(open(cache_path, "r").read())

app = PublicClientApplication(
    client_id=client_id,
    authority=authority,
    token_cache=token_cache
)

accounts = app.get_accounts()
if accounts:
    result = app.acquire_token_silent(scopes, account=accounts[0])
else:
    # fallback to interactive if needed
    # ...

# After acquiring the token:
if token_cache.has_state_changed:
    with open(cache_path, "w") as f:
        f.write(token_cache.serialize())
