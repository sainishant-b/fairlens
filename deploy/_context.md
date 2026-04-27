# Deploy

## What this is for
Setup + deploy notes for the two hosting platforms. Backend → Render (FastAPI + ML compute). Frontend → Appwrite Sites (static React build + CDN). Appwrite Console also hosts Auth and Database for audit history. Env vars wired across both.

## Folder contents
| Subfolder / file pattern | What it holds |
|--------------------------|---------------|
| `render.md` | Render Web Service setup: build command, start command, env vars, free-tier gotchas (cold start, sleep) |
| `appwrite.md` | Appwrite Console setup: project, Database `fairlens_db`, Collection `audit_results` schema + permissions, Sites Git connection or CLI deploy |
| `.env.example` | Template for both backend and frontend env vars. Never commit real `.env` |

## Routing table
| Task | Read | Skip | Skill |
|------|------|------|-------|
| First-time backend deploy | `render.md` | appwrite.md | (suggest) `deploy-render` |
| First-time frontend deploy | `appwrite.md` | render.md | (suggest) `deploy-appwrite` |
| Add new env var | `.env.example`, both md files (sync), `backend/_context.md` or `frontend/_context.md` | engine, components | — |
| Appwrite Collection schema change | `appwrite.md`, `frontend/src/lib/saveAudit.js` | render | — |
| Render cold-start fix | `render.md` (note free-tier sleep behaviour) | frontend | — |
| Rotate Gemini key | Render dashboard env vars, `.env.example` (placeholder only) | frontend | — |

## Conventions
- Backend env vars (Render dashboard): `GEMINI_API_KEY`, any future secrets. Never commit.
- Frontend env vars (Appwrite Site dashboard, prefixed `VITE_`): `VITE_APPWRITE_PROJECT_ID`, `VITE_APPWRITE_DB_ID`, `VITE_RENDER_API_URL`.
- `.env.example` shows variable names + placeholder values only. Real `.env` git-ignored.
- Deploy order on first setup: Appwrite project + DB → Render backend (get URL) → Appwrite Site (paste Render URL into env).
- Render free tier sleeps after 15 min idle. First request takes ~30s. Mention in demo if cold.
- Hackathon CORS = open. Tighten to Appwrite Site origin before any real use.

## Available skills
| Skill | When to use |
|-------|-------------|
| (none yet) | — |

## Suggested skills (not yet built)
| Skill name | Trigger |
|------------|---------|
| `deploy-render` | Push backend + verify endpoint live |
| `deploy-appwrite` | Build + deploy frontend, verify env vars set |
| `appwrite-collection` | Create or migrate Appwrite Collection schema |
