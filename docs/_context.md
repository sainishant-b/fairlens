# Docs

## What this is for
Canonical reference material for the project. Blueprint spec (full hackathon plan), problem statement copy, architecture notes. Nothing here is executable — pure reference. Read before making cross-cutting decisions.

## Folder contents
| Subfolder / file pattern | What it holds |
|--------------------------|---------------|
| `BLUEPRINT.md` | Full FairLens hackathon spec — problem, solution, tech stack, repo layout, build steps, deck outline, video script, README copy. Source of truth for all scope decisions |
| `SKILL_REF.md` | Reference copy of the 3-layered-workspace skill that built this structure |

## Routing table
| Task | Read | Skip | Skill |
|------|------|------|-------|
| Scope question ("does FairLens do X?") | `BLUEPRINT.md` §2, §5 | code | — |
| Tech stack question | `BLUEPRINT.md` §3 | — | — |
| Submission copy needed (problem statement, slide content, video script) | `BLUEPRINT.md` §6, §7, §8 | code | — |
| Re-run workspace audit | `SKILL_REF.md` | — | (suggest) `restructure-workspace` |
| Add new doc (architecture diagram, ADR) | this file | — | — |

## Conventions
- Specs: `SPEC_<name>.md`.
- Architecture decisions: `ADR_<NNNN>_<slug>.md` if added later.
- Plain Markdown only. No HTML.
- Treat `BLUEPRINT.md` as immutable history of original plan. If scope changes, write a new spec or ADR; do not mutate the blueprint.

## Available skills
| Skill | When to use |
|-------|-------------|
| (none yet) | — |

## Suggested skills (not yet built)
| Skill name | Trigger |
|------------|---------|
| `restructure-workspace` | Re-running 3-layered-workspace skill after major scope shift |
