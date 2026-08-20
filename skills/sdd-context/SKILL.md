---
name: sdd-context
description: Assemble the project context for the SDD workflow. Reads AGENTS.md (stack), specs/constitution.md (principles), specs/STATE.md (decisions + handoff), confirmed lessons, docs/scope.md, .coding-standards/, and the artifacts of the target feature. Use before any other sdd-* phase.
---

## What I do

Load the context a phase needs, from the project's source-of-truth files, and summarize it into one
coherent block. Nothing is written.

## Steps

1. Read `AGENTS.md` from the project root (human-owned). Extract the `## Stack` section — stack,
   tooling, test commands — and the `## Git` section — repo topology (`single-repo` vs
   `multirepo`). If `AGENTS.md` is missing, tell the orchestrator to run `grilling` to create it
   before proceeding. If `## Git` is missing, run `detect_repo_topology.py` and flag that it must be
   recorded in `AGENTS.md` before any commit decision.
2. Read `specs/constitution.md` if present. Extract principles and quality bar.
3. Read `specs/STATE.md` if present:
   - `## Decisions` — active `AD-NNN` project-level constraints (read at design/implementation).
   - `## Handoff` — resume snapshot (read on resume only; reconcile against git before acting).
4. **Load confirmed lessons** (only `confirmed`, never `candidate`/`quarantined`):
   `python3 <scripts-dir>/lessons.py list --status confirmed [--scope <area>]`. Apply as guidance.
   Skip silently if no store exists or no code tool is available.
5. Read `.coding-standards/` — list the docs present and extract the ones that apply to the current
   stack and phase. Include a summary (paths + key requirements) in the context block.
6. Read `docs/scope.md` (human-owned initial scope). If missing, stop and ask the human to provide
   it before `/sdd-init`.
7. If a feature name was given, read `specs/<feature>/spec.md`, `design.md`, `tasks.md` and the
   `tasks/` directory; summarize their current state (which tasks are DONE, what is in progress).
8. Read `specs/features.md` if present for the feature backlog.

## Output

Return a compact context block:

- Stack (from AGENTS.md) and test commands.
- **Repo topology** (from `AGENTS.md` `## Git`): `single-repo` (agent drives atomic commits) or
  `multirepo` (human owns all git operations; the agent only reads git and leaves commits to the
  human).
- Coding standards that apply, by path (`.coding-standards/...`) with a one-line summary each.
- Active project decisions (from STATE.md).
- Confirmed lessons that apply.
- Constitution principles that apply.
- Scope summary relevant to the task at hand.
- Target feature state (what exists, what's done, what's next).

## Definition of done

The orchestrator has everything needed to run the next phase without re-reading the files itself.

## Scripts

Validation scripts ship in the harness `scripts/` directory (installed as `.opencode/scripts/` in
the target project). Resolve them as `<skill-dir>/../../scripts/<name>.py`. Never run
`python3 scripts/...` from the consuming project root.