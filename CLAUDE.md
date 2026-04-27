# Workspace Map

## Purpose
FairLens — adversarial bias stress tester for AI hiring/lending models. Hackathon submission for Google Solutions Challenge.

## Workspace Inventory
| Workspace | Folder | What lives here |
|-----------|--------|-----------------|
| backend | `backend/` | FastAPI server, bias engine (adversarial pair generator, disparity scorer, mitigation suggester), pre-trained `.pkl` models, biased training datasets |
| frontend | `frontend/` | React + Vite + Tailwind app, pages (Home/StressTest/Report), components (PairComparison/BiasScore/MitigationCard), Appwrite SDK lib |
| deploy | `deploy/` | Render setup notes, Appwrite Console setup, env templates, deploy commands |
| docs | `docs/` | Blueprint spec, problem statement, architecture notes |

Note: `submission/` (deck, demo video, screenshots) added later in demo phase.

## Naming conventions
- Models:          `<domain>_model.pkl`        (hiring_model.pkl, loan_model.pkl)
- Datasets:        `<domain>_dataset.csv`
- Engine modules:  snake_case `.py`            (adversarial.py, bias_scorer.py)
- React pages:     PascalCase `.jsx`           (StressTest.jsx)
- Specs / briefs:  `SPEC_<name>.md`
- Context files:   `_context.md`               (one per workspace, read before any task)
- Dated assets:    `YYYY-MM-DD_<slug>.<ext>`
- Skills:          `~/.claude/commands/<verb>-<noun>.md`

## Navigation rules
1. Read this file first.
2. Identify which workspace the task belongs to.
3. Read that workspace's `_context.md` before doing anything else.
4. For cross-workspace tasks (e.g. wiring frontend to backend API), read all relevant `_context.md` files before starting.
5. Do not read files outside the active workspace(s) unless a routing table explicitly says to.

## Workspaces
(See each folder's `_context.md` for detail.)

- [backend/_context.md](backend/_context.md)
- [frontend/_context.md](frontend/_context.md)
- [deploy/_context.md](deploy/_context.md)
- [docs/_context.md](docs/_context.md)
