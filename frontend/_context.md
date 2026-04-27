# Frontend

## What this is for
React + Vite + TailwindCSS single-page app. User selects model + protected attribute, hits "Run Stress Test", sees side-by-side prediction comparison + bias score badge + Gemini explanation. Saves audit results to Appwrite DB for history. Hosted on Appwrite Sites (free, CDN, Git auto-deploy). Talks to backend via `VITE_RENDER_API_URL`.

## Folder contents
| Subfolder / file pattern | What it holds |
|--------------------------|---------------|
| `package.json` | Deps: react, vite, tailwindcss, appwrite SDK, recharts (for D3-style viz) |
| `src/App.jsx` | Router + layout shell |
| `src/pages/Home.jsx` | Landing — model + attribute selector, demo intro |
| `src/pages/StressTest.jsx` | Main tester — fires `/stress-test`, renders results |
| `src/pages/Report.jsx` | Detailed Bias Exposure Report (post-test) |
| `src/components/PairComparison.jsx` | Side-by-side variant cards with score bars |
| `src/components/BiasScore.jsx` | Big badge — LOW/MEDIUM/HIGH + disparity % + disadvantaged group |
| `src/components/MitigationCard.jsx` | Renders backend mitigation suggestions |
| `src/lib/appwrite.js` | Appwrite Client / Account / Databases setup |
| `src/lib/saveAudit.js` | `saveAuditResult(report, model, attribute)` writes to `audit_results` collection |

## Routing table
| Task | Read | Skip | Skill |
|------|------|------|-------|
| New page | `App.jsx` (router), `pages/` | backend, deploy | — |
| New visualisation | `components/`, recharts docs | backend internals | — |
| Wire new backend endpoint into UI | `pages/StressTest.jsx` (fetch pattern), `backend/_context.md` routing table | deploy | — |
| Appwrite DB schema change | `lib/saveAudit.js`, `deploy/appwrite.md` | backend, engine | — |
| Auth flow | `lib/appwrite.js` (Account), new page | backend, engine | — |
| Style/theme tweak | `tailwind.config.js`, components | backend, lib | — |
| Deploy frontend | `deploy/appwrite.md` | backend | — |

## Conventions
- Pages: PascalCase `.jsx` in `src/pages/`.
- Components: PascalCase `.jsx` in `src/components/`. Pure presentational where possible — fetching lives in pages.
- Library / SDK wrappers: `src/lib/<name>.js`, lowercase. One concern per file (`appwrite.js` = client setup, `saveAudit.js` = one DB op).
- Env vars: prefix with `VITE_` so Vite exposes them to client. Never put secrets here — backend owns secrets.
  - `VITE_APPWRITE_PROJECT_ID`
  - `VITE_APPWRITE_DB_ID`
  - `VITE_RENDER_API_URL`
- Tailwind only — no CSS modules, no styled-components. Keep class strings inline.
- Demo must work zero-upload. Pre-load `DEMO_RECORD` constant in `StressTest.jsx`. Judges click → see bias.
- Bias reveal moment is the product. Do not bury it in UI chrome.
- After any successful `/stress-test` response: call `saveAuditResult()` so history populates.

## Available skills
| Skill | When to use |
|-------|-------------|
| (none yet) | — |

## Suggested skills (not yet built)
| Skill name | Trigger |
|------------|---------|
| `add-bias-domain` | New model domain — adds option to selector + handles new feature schema |
| `record-demo` | Cuts a 2-min demo video following script in `submission/` (when added) |
