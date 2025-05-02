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

def get_access_token():
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

    # Return the token
    if "access_token" in result:
        print("✅ Access token acquired.")
        return result["access_token"]
    else:
        print("❌ Failed to acquire access token:")
        print(result)
        exit(1)
