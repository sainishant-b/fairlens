# Appwrite Deploy — Frontend + DB

## Console setup (one-time, manual)

1. cloud.appwrite.io → Create Project → name `fairlens`. Copy **Project ID**.
2. Database → Create → name `fairlens_db`. Copy **Database ID**.
3. Inside `fairlens_db` → Create Collection → ID `audit_results`.
4. Add attributes to `audit_results`:
   | Key | Type | Required |
   |-----|------|----------|
   | `model` | string (255) | yes |
   | `attribute` | string (255) | yes |
   | `bias_level` | string (16) | yes |
   | `disparity` | float | yes |
   | `disadvantaged_group` | string (255) | yes |
   | `timestamp` | string (64) | yes |
5. Permissions on Collection: `Any` → Create + Read (hackathon demo only — tighten later).

## Frontend deploy

### Option A — Git auto-deploy (recommended)
1. Console → Sites → Create Site → Connect Git → select repo.
2. **Root directory:** `frontend`
3. **Build command:** `npm run build`
4. **Output directory:** `dist`
5. **Env vars** (Site dashboard):
   - `VITE_APPWRITE_PROJECT_ID`
   - `VITE_APPWRITE_DB_ID`
   - `VITE_RENDER_API_URL`
6. Deploy.

### Option B — CLI
```bash
cd frontend
npm run build
npm install -g appwrite-cli
appwrite login
appwrite deploy site
```

## Verify
- Open Site URL. Home page loads.
- Run a stress test. Check Appwrite Console → Database → `audit_results` — new doc appears per test.
- If fetch fails: check browser console for CORS. Backend Render service must allow Appwrite Site origin (currently `*` for hackathon).

## Notes
- Project ID and DB ID are public-safe (they're in `VITE_*` vars). Permissions enforce access.
- Auth (`account` from `appwrite.js`) is wired but not required for demo. Add login flow later if needed.
- Schema change = update Collection in Console + update `frontend/src/lib/saveAudit.js` payload shape together.
