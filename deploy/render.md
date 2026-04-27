# Render Deploy — Backend

## One-time setup

1. Push `backend/` to GitHub (monorepo OK — Render supports Root Directory).
2. render.com → New → Web Service → Connect GitHub repo.
3. **Root Directory:** `backend`
4. **Environment:** Python 3
5. **Build command:**
   ```
   pip install -r requirements.txt && python data/generate_biased_models.py
   ```
6. **Start command:**
   ```
   uvicorn main:app --host 0.0.0.0 --port 10000
   ```
7. **Environment variables:**
   - `VOIDAI_API_KEY` = your VoidAI key (required)
   - `VOIDAI_BASE_URL` = `https://api.voidai.app/v1` (default)
   - `VOIDAI_MODEL` = `gpt-5-mini` (default)
8. **Plan:** Free tier (sleeps after 15 min idle, ~30s cold start).
9. Deploy. Copy the URL — paste into Appwrite Site env as `VITE_RENDER_API_URL`.

## Verify

```bash
curl -X POST https://YOUR-APP.onrender.com/stress-test \
  -H "Content-Type: application/json" \
  -d '{"record":{"years_experience":7,"education_level":3,"num_skills":12,"gender_encoded":0,"name_origin":0},"model":"hiring","attribute":"name"}'
```

Should return JSON with `pairs`, `predictions`, `bias_report`.

## Notes
- Free tier cold start kills demo flow. Hit endpoint once before demo to wake.
- `.pkl` files are generated at build time by the training script — not committed to git. Build log will show "Biased hiring model saved."
- Python pinned to 3.11.9 via `render.yaml`. Change there if needed.
- CORS is wide open. Lock to Appwrite Site origin before any non-demo use.
- LLM provider is OpenAI-compatible — swap `VOIDAI_BASE_URL` / `VOIDAI_MODEL` env vars to switch providers without code changes.
