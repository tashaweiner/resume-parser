# interactive_onedrive_auth.py
import os
import requests
import webbrowser
from msal import PublicClientApplication
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("ONEDRIVE_CLIENT_ID")
tenant_id = os.getenv("ONEDRIVE_TENANT_ID")  # Usually 'common' works here too
authority = f"https://login.microsoftonline.com/{tenant_id}"

scopes = ["Files.Read"]  # You can later upgrade this to Files.ReadWrite if needed

app = PublicClientApplication(client_id=client_id, authority=authority)

# Try getting a cached token first
accounts = app.get_accounts()
if accounts:
    result = app.acquire_token_silent(scopes, account=accounts[0])
else:
    # Launch a browser for user to sign in
    flow = app.initiate_device_flow(scopes=scopes)
    if "user_code" not in flow:
        raise Exception("Failed to create device flow")

    print(f"Go to {flow['verification_uri']} and enter the code: {flow['user_code']}")
    webbrowser.open(flow['verification_uri'])
    result = app.acquire_token_by_device_flow(flow)

# Use the token to access OneDrive

if "access_token" in result:
    access_token = result["access_token"]
    print("✅ Access token acquired.")
else:
    print("❌ Failed to get access token:")
    print(result)
# access_token = result["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}

# Adjust this path to your folder name
url = "https://graph.microsoft.com/v1.0/me/drive/root:/Resumes:/children"

res = requests.get(url, headers=headers)
print(f"🔁 Status: {res.status_code}")
files = res.json().get("value", [])
print(f"📄 Found {len(files)} items in the Resumes folder")

# for f in files:
#     print(f"📄 {f['name']}")
# # Download PDFs
for file in files:
    if file["name"].endswith(".pdf"):
        download_url = file["@microsoft.graph.downloadUrl"]
        content = requests.get(download_url).content
        with open(f"backend/resumes/{file['name']}", "wb") as f:
            f.write(content)
            print(f"✅ Downloaded: {file['name']}")
