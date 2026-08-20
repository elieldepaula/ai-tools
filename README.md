# Harness — SDD for OpenCode (Laravel + React/Vue)

A reusable OpenCode harness that runs an **auto-sized Spec-Driven Development (SDD)** workflow on
PHP/Laravel backends with React and VueJs frontends. It ships a primary orchestrator agent,
read-only specialist subagents, one skill per SDD phase, deterministic Python validation scripts,
and thin slash commands — all plain markdown in OpenCode's native `agents/`, `skills/`, and
`commands/` format.

## Install

1. Clone this repository.
2. Run `./install.sh` — it builds the bundle in `dist/.opencode/` and the coding standards in
   `dist/.coding-standards/` (gitignored).
3. Copy the generated folders into the root of your target project:

   ```bash
   cp -R dist/.opencode /path/to/your/project/.opencode
   cp -R dist/.coding-standards /path/to/your/project/.coding-standards
   ```

4. In the target project, create the human-owned `docs/` folder (gitignored) and provide
   `docs/scope.md` describing the initial project scope.
5. Run `/sdd-init` in OpenCode.

Re-run `install.sh` and recopy to update the harness in your projects.

## Project layout (target project)

```
<project>/
├── AGENTS.md          # human-owned; "## Stack" section declares the stack
├── docs/              # gitignored, human-owned
│   └── scope.md       # initial project scope (required before /sdd-init)
├── specs/             # committed — source of truth (SDD artifacts)
│   ├── constitution.md
│   ├── features.md    # feature backlog derived from the scope
│   ├── STATE.md       # Decisions (AD-NNN log) + Handoff (resume snapshot)
│   ├── lessons.json   # machine-owned lessons store (edit via lessons.py)
│   ├── LESSONS.md     # rendered lessons playbook (auto)
│   └── <feature>/
│       ├── spec.md          # EARS ACs + requirement IDs + assumptions
│       ├── design.md        # Large/Complex only
│       ├── tasks.md         # Test Coverage Matrix + Gate Commands + index
│       ├── validation.md    # Verifier report (PASS/FAIL + evidence)
│       └── tasks/
│           └── <task-id>-<slug>.md    # one file per task
├── .coding-standards/  # coding standards (installed bundle)
└── .opencode/         # installed harness (agents/, skills/, commands/, scripts/)
```

`docs/` and `dist/` are gitignored. `specs/` is committed.

## Workflow (auto-sized)

Every feature is sized on entry. **Small/Medium** skip design and tasks (implementation lists atomic
steps inline); **Large/Complex** run the full pipeline.

1. `/sdd-init` — reads `docs/scope.md`, grills the human (creates `AGENTS.md` with `## Stack` if
   missing), generates `specs/constitution.md`, `specs/STATE.md`, the lessons store, and
   `specs/features.md`.
2. `/sdd-spec <feature>` — architect drafts `spec.md` (EARS ACs, requirement IDs); grilling resolves
   ambiguity; the closure gate `validate_spec.py` runs before human approval.
3. `/sdd-plan <feature>` — (Large/Complex) architect designs `design.md`; project-level decisions
   become `AD-NNN` entries in `specs/STATE.md`.
4. `/sdd-tasks <feature>` — (Large/Complex) breaks the plan into tasks with a Test Coverage Matrix;
   the pre-approval gate `validate_tasks.py` runs before human approval.
5. `/sdd-checklist` and `/sdd-analyze` — quality gates before implementation.
6. `/sdd-implement <feature>` — delegates tasks to `backend-dev` / `react-dev` / `vue-dev`, runs gate
   checks, enforces atomic Conventional Commits (`check_commit.py`) in a **single-repo** or hands the
   human a commit-ready summary in a **multirepo**, marks tasks `DONE`.
7. `/sdd-verify <feature>` — an independent `verifier` subagent (author != verifier) runs a
   spec-anchored coverage check + lightweight discrimination sensor, writes `validation.md`.
8. `/sdd-converge <feature>` — `reviewer` verifies against spec/design/tasks; the completion gate
   `validate_state.py` runs; grounded failures become lessons via `lessons.py`.
9. `/sdd-resume <feature>` — resumes a feature by reconciling `specs/STATE.md` Handoff against git
   and `tasks.md`.

## Agents

| Agent          | Mode    | Edit | Role                                                     |
|----------------|---------|------|----------------------------------------------------------|
| `sdd`          | primary | yes  | Orchestrates the SDD flow; materializes all artifacts    |
| `architect`    | subagent| no   | Scope/spec/design/task analysis (read-only reports)      |
| `backend-dev`  | subagent| yes  | PHP/Laravel implementation                               |
| `react-dev`    | subagent| yes  | React implementation                                     |
| `vue-dev`      | subagent| yes  | VueJs implementation                                     |
| `tester`       | subagent| no   | Runs test/lint suites, reports failures                  |
| `reviewer`     | subagent| no   | Reviews artifacts and code against requirements          |
| `verifier`     | subagent| no   | Independent verification (author != verifier) + sensor   |

Domain boundaries (backend vs frontend) are enforced by agent prompts; `tester`/`reviewer`/`architect`/
`verifier` are read-only.

## Skills

- `grilling` — round-by-round interview to eliminate ambiguity; usable any time.
- `sdd-context` — assembles project context (AGENTS.md + constitution + STATE.md decisions +
  confirmed lessons + coding standards + docs/scope.md).
- `sdd-init` — bootstrap: AGENTS.md (grilling if absent) → scope analysis → constitution + STATE.md +
  lessons + features.
- `sdd-spec`, `sdd-plan`, `sdd-tasks` — artifact-producing phases (auto-sized).
- `sdd-checklist`, `sdd-analyze` — quality gates.
- `sdd-implement`, `sdd-verify`, `sdd-converge` — implementation, independent verification, and
  convergence.
- `sdd-resume` — resume in-progress features.

## Scripts (deterministic gates)

Python validation scripts ship in `scripts/` (installed as `.opencode/scripts/`). They make the
structural gates checkable by code instead of model memory. Pure standard library — no dependencies.

| Script | Gate | Runs when |
|--------|------|-----------|
| `validate_spec.py` | EARS-shaped ACs, required sections, assumption closure, requirement IDs | Before spec approval (`sdd-spec`) |
| `validate_tasks.py` | Granularity, dependency coherence, Tests/Gate fields, index/detail parity | Before task approval (`sdd-tasks`) |
| `check_commit.py` | Conventional Commits 1.0.0 | Per atomic commit (`sdd-implement`) |
| `validate_state.py` | `validation.md` exists, PASS verdict, `file:line` evidence | Feature completion (`sdd-converge`) |
| `lessons.py` | Lessons bookkeeping: add/list/promote/penalize/prune | After validation; loaded at spec/design |

A non-zero exit means STOP and fix before proceeding.

## Commands

`/sdd-init`, `/sdd-install`, `/sdd-context`, `/sdd-spec`, `/sdd-plan`, `/sdd-tasks`, `/sdd-checklist`,
`/sdd-analyze`, `/sdd-implement`, `/sdd-verify`, `/sdd-converge`, `/sdd-resume`.

## Conventions

- All agent prompts, skills, and commands are written in English.
- Default test stack: Pest (Laravel), Vitest + Testing Library (React/Vue), Playwright (e2e).
  Override in `AGENTS.md` under `## Stack`.
- Stack is declared by the human in the target project's `AGENTS.md`; the harness never hardcodes it.
- Git ownership follows the repo topology recorded in `AGENTS.md` under `## Git` (set by `/sdd-init`
  via `scripts/detect_repo_topology.py` and confirmed with the human): a **single-repo** lets the
  agent drive atomic Conventional Commits per task; a **multirepo** (the root is not its own git work
  tree) puts all git operations in the human's hands — the agent only reads git and hands over a
  commit-ready summary. Read-only git (`status`/`diff`/`log`) is always allowed.
- Coding standards live in `.coding-standards/` and are referenced by path from agents and skills.
- Acceptance criteria are written in EARS notation with a SHALL and requirement IDs
  (`CATEGORY-NNN`).

## Out of scope

- Git is human-managed in multirepo projects (no agent git writes there); in single-repo projects
  atomic Conventional Commits are enforced per task. Branch/push strategy is always human-owned.
- No component selection in `install.sh` — the full bundle is built.
- `docs/` is human territory; the harness only reads `docs/scope.md`.