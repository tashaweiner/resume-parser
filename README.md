# Resume Parser with OneDrive + OpenAI

This Python project connects to a corporate OneDrive (via Microsoft Graph), downloads PDF resumes, extracts their text, and uses OpenAI to convert them into structured JSON format.

---

## 🚀 Features

- Connects to OneDrive using Microsoft Graph API
- Downloads PDF resumes from a specified folder
- Extracts text using `pdfplumber`
- Sends content to OpenAI to generate structured JSON
- Saves parsed output locally or back to OneDrive (optional)

---

## ⚙️ Setup Instructions

### 1. 🔐 Azure App Registration (One-Time)

1. Go to [Azure Portal](https://portal.azure.com)
2. Search for **"App registrations"** → Click **"New registration"**
3. Fill in:
   - Name: `ResumeParserApp`
   - Supported account types: "Accounts in this organizational directory only"
   - Redirect URI: leave blank
4. Click **Register**

### 2. 🔑 Get the following credentials:

- **Client ID**
- **Tenant ID**
- **Client Secret** (under "Certificates & secrets")

---

### 3. 🔒 Set Permissions for Microsoft Graph

In the Azure App:
- Go to **API permissions** → Add these:
  - `Files.Read`
  - `Files.Read.All`
- Click **"Grant admin consent"**

---

### 4. 🗂️ Project Structure

