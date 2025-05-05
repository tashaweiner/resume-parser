# backend/main.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router  # ✅ absolute import
from fastapi.middleware.cors import CORSMiddleware
from search.routes import router as search_router


app = FastAPI()
app.include_router(api_router)
app.include_router(search_router, prefix="/search")

# Allow requests from frontend (adjust if deploying elsewhere)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://resume-parser-peach.vercel.app"
],  # or ["*"] during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
