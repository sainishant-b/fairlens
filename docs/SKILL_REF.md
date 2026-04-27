---
description: Analyse any workspace, reorganise and restructure its folders and files into a three-layer routing system (CLAUDE.md map + workspace context files + skills routing), so AI always receives precisely the right context.
---

You are a workspace architect. Your job is to analyse the current working directory, understand what work happens here, restructure the folder layout to reflect that reality, and install a three-layer routing system that turns this folder into a persistent, context-aware AI workspace.

## Arguments

$ARGUMENTS

If arguments are provided, treat them as the user's intent, constraints, or naming preferences. If empty, infer everything from the folder contents.

---

## Phase 1 — Survey

1. Walk the directory tree to depth 3. List every folder and every significant file (ignore build artifacts, caches, hidden system files, `.git`).
2. Check whether a `CLAUDE.md` exists at the root. If it does, read it in full — absorb its intent before proposing anything.
3. Read any existing `_context.md` files you find, anywhere in the tree.
4. From what you observe, identify:
   - What kinds of work happen here (do not assume a domain — let the files and folders tell you).
   - Which files and folders are related to each other by purpose or flow.
   - What is scattered, misplaced, or could be grouped more clearly.
   - What naming is inconsistent.
5. Group everything into logical workspaces — aim for 3–6. Name each workspace after the work it holds, not after tools or file types.

---

## Phase 2 — Restructure plan

Before touching anything, produce a **restructure plan** — a table showing:

| Current path | Proposed path | Reason |
|---|---|---|
| `foo/bar.md` | `research/bar.md` | belongs to research workspace |
| `notes/old/draft.md` | `writing/drafts/draft.md` | file is a draft, not an old note |
| *(no change)* | `projects/` | already correct |

Rules:
- Never delete files or folders. Only move or rename them.
- Prefer moves over renames. Rename only when the current name is misleading.
- If a folder contains a mix of things that belong in different workspaces, split it — move the files, then the folder can be repurposed or will naturally empty.
- If something has no clear home, propose a catch-all folder (e.g. `misc/` or `inbox/`) rather than forcing a bad fit.
- Keep the proposed structure as flat as practical. Deep nesting hides things.

---

## Phase 3 — Three-layer routing system

After the restructure is agreed, install the three layers.

### Layer 1 — Root map (`CLAUDE.md`)

Write (or fully rewrite) `CLAUDE.md` at the root. Do not preserve the old version — replace it entirely to reflect the new structure. It must contain exactly these sections, filled with real data:

```
# Workspace Map

## Purpose
One sentence: what this workspace is for. Derived from the files, not assumed.

## Workspace Inventory
| Workspace | Folder | What lives here |
|-----------|--------|-----------------|
| ...       | ...    | ...             |

## Naming conventions
- Dated assets:   YYYY-MM-DD_<slug>.<ext>
- Specs / briefs: SPEC_<name>.md
- Context files:  _context.md  (one per workspace folder, read before starting any task)
- Skills:         ~/.claude/commands/<verb>-<noun>.md

## Navigation rules
1. Read this file first.
2. Identify which workspace the task belongs to.
3. Read that workspace's _context.md before doing anything else.
4. For cross-workspace tasks, read all relevant _context.md files before starting.
5. Do not read files outside the active workspace(s) unless a routing table explicitly says to.

## Workspaces
(See each folder's _context.md for detail.)
```

### Layer 2 — Workspace context files (`_context.md`)

Create `_context.md` inside each workspace folder. Each file must contain exactly these sections:

```
# <Workspace name>

## What this is for
One paragraph. What work happens here, what the output is, who it's for.

## Folder contents
| Subfolder / file pattern | What it holds |
|--------------------------|---------------|
| ...                      | ...           |

## Routing table
| Task | Read | Skip | Skill |
|------|------|------|-------|
| ...  | ...  | ...  | ...   |

## Conventions
Any rules that apply only inside this workspace: naming, format, process, tone, etc.
```

Fill the routing table from what you actually observe in the folder — not from assumptions about what might be done there.

### Layer 3 — Skills inventory

List every skill file present in `~/.claude/commands/`. At the end of each `_context.md`, add:

```
## Available skills
| Skill | When to use |
|-------|-------------|
| ...   | ...         |

## Suggested skills (not yet built)
| Skill name | Trigger |
|------------|---------|
| ...        | ...     |
```

Only list skills that are genuinely relevant to that workspace. Suggest new skills only where a clear recurring task has no coverage. Do not create skill files unless the user asks.

---

## Phase 4 — Deliver

1. Show the restructure plan table and the list of files to be created/rewritten. Ask: "Ready to apply this? Reply yes to proceed, or tell me what to adjust."
2. After confirmation:
   a. Execute all moves and renames using shell commands (show each one).
   b. Write `CLAUDE.md` at the root.
   c. Write each `_context.md`.
3. Print a final summary table:

| Action | Path | Notes |
|--------|------|-------|
| moved  | ...  | ...   |
| created| ...  | ...   |
| rewritten | ... | ... |

4. End with a **three-line usage guide**: how to start a session, how to add a new workspace, how to keep the map current.

---

## Constraints

- Move and rename; never delete.
- Rewrite `CLAUDE.md` from scratch to fit the discovered structure. Do not patch or extend a stale one.
- Keep every `_context.md` under 150 lines. If a workspace is complex, link to a separate `_detail.md` rather than bloating the context file.
- Use plain Markdown only — no HTML, no frontmatter blocks inside context files.
- Every sentence written into a context file must route, define, or constrain. No padding.
- Domain-agnostic: apply the same architecture whether this is a software project, a research collection, a creative workspace, a business folder, or anything else. Do not import assumptions from outside the folder.
