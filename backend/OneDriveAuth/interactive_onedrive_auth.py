import os
import requests
import webbrowser
from msal import PublicClientApplication, SerializableTokenCache
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("ONEDRIVE_CLIENT_ID")
tenant_id = os.getenv("ONEDRIVE_TENANT_ID") or "common"
authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["Files.Read"]

# Setup persistent token cache
token_cache_path = "token_cache.bin"
cache = SerializableTokenCache()

if os.path.exists(token_cache_path):
    with open(token_cache_path, "r") as f:
        cache.deserialize(f.read())

app = PublicClientApplication(
    client_id=client_id,
    authority=authority,
    token_cache=cache
)

# Try silent auth
accounts = app.get_accounts()
result = None

if accounts:
    print("🔐 Found cached account. Trying silent login...")
    result = app.acquire_token_silent(scopes, account=accounts[0])

# If silent fails, do interactive device login
if not result:
    print("🔑 No cached token found or expired. Starting device login flow...")
    flow = app.initiate_device_flow(scopes=scopes)
    if "user_code" not in flow:
        raise Exception("❌ Failed to initiate device flow.")

    print(f"➡️  Go to {flow['verification_uri']} and enter the code: {flow['user_code']}")
    webbrowser.open(flow["verification_uri"])
    result = app.acquire_token_by_device_flow(flow)

# Save cache if it changed
if cache.has_state_changed:
    with open(token_cache_path, "w") as f:
        f.write(cache.serialize())

# Use token
if "access_token" in result:
    access_token = result["access_token"]
    print("✅ Access token acquired.")
else:
    print("❌ Failed to acquire access token:")
    print(result)
    exit(1)

# Query files in the Resumes folder
headers = {"Authorization": f"Bearer {access_token}"}
url = "https://graph.microsoft.com/v1.0/me/drive/root:/Resumes:/children"

res = requests.get(url, headers=headers)
print(f"🔁 Status: {res.status_code}")
files = res.json().get("value", [])
print(f"📄 Found {len(files)} items in the Resumes folder")

os.makedirs("backend/resumes", exist_ok=True)

for file in files:
    if file["name"].endswith(".pdf"):
        local_path = f"backend/resumes/{file['name']}"
        
        if os.path.exists(local_path):
            print(f"⏭️  Skipping existing file: {file['name']}")
            continue

        download_url = file["@microsoft.graph.downloadUrl"]
        content = requests.get(download_url).content
        with open(local_path, "wb") as f:
            f.write(content)
            print(f"✅ Downloaded: {file['name']}")