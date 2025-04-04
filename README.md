# 📄 Resume Parser & AI Search Tool

A full-stack resume parser and search tool powered by OpenAI. This app helps you convert resumes into structured JSON data and intelligently search and rank them based on any custom query — perfect for daily recruiter use.

---

## ✨ Features

- 🧠 Parses PDF resumes into structured JSON using OpenAI (GPT-4 or GPT-3.5)
- 📁 Automatically skips already-parsed resumes
- 🔍 Ranks candidates by relevance to a search query (using GPT)
- 🌐 FastAPI backend with `/resumes` and `/search` endpoints
- 💻 React frontend to browse and search resumes (in progress)

---

## 📂 Project Structure

```
resume_parser/
├── backend/
│   ├── main.py             # FastAPI app entry
│   ├── api.py              # API endpoints: /resumes, /search
│   ├── parser/
│   │   └── parseFiles.py   # Converts PDFs → JSON using OpenAI
│   ├── search/
│   │   └── searchParsed.py # Ranks resumes by relevance using GPT
│   ├── output/             # Parsed resume JSONs (ignored by Git)
│   ├── resumes/            # Drop raw PDF resumes here
│   ├── requirements.txt
│   └── .env                # Stores your OpenAI API key
│
├── frontend/               # React app (in progress)
│   └── ...
└── README.md
```

---

## 🔧 How to Run the Backend

### 📄 1. Set up environment
```bash
cd resume_parser/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🔐 2. Set your OpenAI API key
```bash
echo "OPENAI_API_KEY=sk-REPLACE_ME" > .env
```

### 🚀 3. Start the FastAPI server
Run this from the root of your project:
```bash
uvicorn backend.main:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore API endpoints.

---

## 🔹 How to Use Each File in Backend

### 📁 Parse PDF Resumes to JSON
```bash
python backend/parser/parseFiles.py
```
- Reads PDFs in `resumes/`
- Converts to JSON using OpenAI
- Saves to `output/`
- Skips files already processed

### 🔍 Search for Relevant Candidates
```bash
python backend/search/searchParsed.py
```
- Prompts you for a question
- Uses OpenAI to score resumes for relevance
- Prints ranked list

---

## 🌐 API Endpoints

### `GET /resumes`
Returns a list of all parsed resumes.

### `POST /search`
Send a query in the body:
```json
{
  "question": "Looking for a Python developer with React experience"
}
```
Returns ranked list of matching resumes.

---

## 💻 How to Run the Frontend (React)
```bash
cd resume_parser/frontend
npm install
npm start
```
- Opens at [http://localhost:3000](http://localhost:3000)
- Will connect to backend at [http://localhost:8000](http://localhost:8000)

---

## 🚀 Coming Soon
- Resume upload via UI
- Hybrid AI + keyword search
- Admin dashboard
- OneDrive integration (optional)

---

## 🔒 Environment Variables
In `backend/.env`:
```
OPENAI_API_KEY=sk-REPLACE_ME
```

---

## 📅 .gitignore Suggestions
```
backend/output/
backend/resumes/
backend/.env
backend/venv/
__pycache__/
```

---

## 🧠 Built With
- Python + FastAPI (backend)
- React (frontend)
- OpenAI (GPT-4 / GPT-3.5)
- PyMuPDF (PDF parsing)
```
