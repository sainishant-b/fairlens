# FairLens — Adversarial Bias Stress Tester

Expose hidden discrimination in AI systems before they impact real people.

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python data/generate_biased_models.py
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## How It Works
1. Select a model (hiring, loan approval).
2. Select a protected attribute (name, zip code).
3. FairLens generates identical records differing only in that attribute.
4. Runs all variants through the model.
5. Scores and visualises the disparity.
6. AI explains the impact in plain English.

## Built With
- FastAPI, scikit-learn — hosted on Render
- React, Vite, TailwindCSS — hosted on Appwrite Sites
- Appwrite Auth + Database — audit history storage
- VoidAI Gemini-flash-2.5 (Gemini-compatible) for plain-English bias explanations

## Repo Layout
- `backend/` — FastAPI + bias engine + ML models
- `frontend/` — React/Vite app
- `deploy/` — Render + Appwrite setup notes
- `docs/` — full blueprint, architecture, specs

See [CLAUDE.md](CLAUDE.md) for workspace routing.
