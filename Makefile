# file for Resume Parser App

# Run backend FastAPI server
# run-backend:
# 	cd backend && PYTHONPATH=.. source venv/bin/activate && uvicorn main:app --reload
run-backend:
	cd backend && PYTHONPATH=. ../venv/bin/python -m uvicorn main:app --reload  

# Setup backend (runs setup.sh)
setup-backend:
	cd backend && bash setup.sh && cd ..

# Run React frontend
run-frontend:
	cd frontend && npm install && npm start


# Run both backend and frontend (separate terminals recommended)
dev:
	@echo "👉 In one terminal, run:  run-backend"
	@echo "👉 In another terminal, run:  run-frontend"

# Download resumes from OneDrive
fetch-resumes:
	python backend/onedrive/download_resumes.py

# Authenticate with OneDrive (only needed once)
auth-onedrive:
	python backend/onedrive/interactive_onedrive_auth.py
backfill-embeddings:
	venv/bin/python backend/scripts/backfill_embeddings.py
