# Collaborative Docs – Starter (FastAPI + React)

## Backend (FastAPI)
### Run (Dev)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
### API Highlights
- POST /auth/register {email, name, password}
- POST /auth/login {email, name, password} -> Bearer token
- CRUD /documents (Authorization: Bearer <token>)
- WS /ws/docs/{doc_id} – broadcast-only MVP

## Frontend (React + Vite)
### Setup
```bash
cd frontend
npm install
npm run dev
```
Configure `VITE_API_URL` in `.env` if needed.

## Run Everything from One Script

After installing backend requirements (`pip install -r backend/requirements.txt`) and frontend dependencies (`npm --prefix frontend install`), install `pywebview` and run:

```bash
pip install pywebview
python run_docs.py
```

The launcher uses your current Python interpreter for `uvicorn` and the proper `npm` binary on Windows, then opens a desktop window to the Vite dev server.
