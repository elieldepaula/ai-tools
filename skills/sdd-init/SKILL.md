---
name: sdd-init
description: Bootstrap a project for SDD. Reads docs/scope.md, creates AGENTS.md (via grilling if missing), generates specs/constitution.md, initializes specs/STATE.md (decisions + handoff) and the lessons store, and derives specs/features.md. Run once per project.
---

## What I do

Initialize the project's SDD foundation: the human-owned context (`AGENTS.md`, `docs/scope.md`),
the constitution, the decision log, the lessons store, and the feature backlog. This runs once,
before feature specs exist.

## Prerequisites

- `docs/scope.md` exists (human-owned). If missing, ask the human to create it first — the harness
  never invents the initial scope.

## Steps

1. **AGENTS.md** — if missing, run `grilling` to interview the human and produce `AGENTS.md` with a
   `## Stack` section (and conventions). If it exists, read it; use `grilling` only to resolve
   remaining ambiguity. Confirm which `.coding-standards/` docs apply to the stack and record that
   in `AGENTS.md`/the constitution. If the docs are missing, tell the human to install them via
   `install.sh`.
2. **Git topology** — run `python3 <scripts-dir>/detect_repo_topology.py` at the project root. It
   prints `single-repo` (the root is its own git work tree → the agent may drive atomic commits)
   or `multirepo` (nested/absent repos → the human owns all git operations). Confirm the result
   with the human via `grilling`, then record it in `AGENTS.md` under `## Git` (create the section
   if missing). Never let the agent commit in a `multirepo`.
3. **Scope analysis** — load `sdd-context`, then analyze `docs/scope.md` with the `architect`
   subagent: goal, boundaries, module map, assumptions. Use `grilling` to clarify anything ambiguous
   before locking decisions.
4. **Constitution** — generate `specs/constitution.md` following the shipped template. Fill it from
   `AGENTS.md` (stack, test commands, git topology) and the grilling answers (principles, quality
   bar, delegation rules). Cross-check against `.coding-standards/` and reference the ones that
   apply. Present it for human approval/edit.
5. **Decision log** — initialize `specs/STATE.md` with `## Decisions` (append-only AD-NNN log) and
   `## Handoff` (empty resume snapshot). See the memory layout below.
6. **Lessons store** — initialize it: `python3 <scripts-dir>/lessons.py init`. Creates
   `specs/lessons.json` (machine-owned) and `specs/LESSONS.md` (rendered playbook).
7. **Feature backlog** — derive `specs/features.md` from the scope: candidate features (name +
   one-line description + source scope section). Have the human confirm/adjust the list.
8. Report the result and the next step: creating a feature spec via `/sdd-spec <feature>`.

## STATE.md layout

```markdown
# STATE

## Decisions

### AD-001
- **Decision**: [one sentence]
- **Reason**: [why chosen]
- **Trade-off**: [what was given up]
- **Scope**: [which features/packages/layers this governs]
- **Date**: YYYY-MM-DD
- **Status**: active | superseded by AD-NNN

## Handoff
- **Feature**: -
- **Phase / Task**: -
- **Completed**: -
- **In-progress** (file:line): -
- **Next step**: -
- **Blockers**: -
- **Uncommitted files**: -
- **Branch**: -
```

**Section-scoped write rule (critical):** `## Decisions` is append-only — writes there never touch
`## Handoff`. Pause writes replace only the `## Handoff` body (between its header and the next `##`
or EOF). Never overwrite the whole file.

## Definition of done

`AGENTS.md` (or confirmed existing), `specs/constitution.md` (human-approved),
`specs/STATE.md` (decisions log + handoff), `specs/lessons.json` (initialized),
`specs/features.md` (human-confirmed). Human approves each artifact before moving on.

## Scripts

Validation scripts ship in the harness `scripts/` directory (installed as `.opencode/scripts/` in
the target project). Resolve them as `<skill-dir>/../../scripts/<name>.py`. Never run
`python3 scripts/...` from the consuming project root.