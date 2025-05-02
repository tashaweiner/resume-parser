# # backend/onedrive/download.py
# import os
# import requests
# from .interactive_onedrive_auth import get_access_token

# def download_resumes():
#     access_token = get_access_token()
#     headers = {"Authorization": f"Bearer {access_token}"}
#     url = "https://graph.microsoft.com/v1.0/me/drive/root:/Resumes:/children"

#     res = requests.get(url, headers=headers)
#     print(f"🔁 Status: {res.status_code}")
#     files = res.json().get("value", [])
#     print(f"📄 Found {len(files)} items in the Resumes folder")

#     os.makedirs("backend/resumes", exist_ok=True)

#     for file in files:
#         if file["name"].endswith(".pdf"):
#             local_path = f"backend/resumes/{file['name']}"
            
#             if os.path.exists(local_path):
#                 print(f"⏭️  Skipping existing file: {file['name']}")
#                 continue

#             download_url = file["@microsoft.graph.downloadUrl"]
#             content = requests.get(download_url).content
#             with open(local_path, "wb") as f:
#                 f.write(content)
#                 print(f"✅ Downloaded: {file['name']}")

# if __name__ == "__main__":
#     download_resumes()
