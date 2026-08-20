---
name: sdd-tasks
description: Break a feature plan into granular, dependency-ordered, testable tasks — only for Large/Complex features. Produces specs/<feature>/tasks.md (index + Test Coverage Matrix + Gate Check Commands) and specs/<feature>/tasks/<task-id>-<slug>.md detail files. Runs the deterministic pre-approval gate (validate_tasks.py) before human approval. Skip for Small/Medium features (tasks implicit in sdd-implement). Use with a feature name.
---

## What I do

Turn the approved design into concrete work items for Large/Complex features: a task index
(`tasks.md`) plus one detailed file per task under `tasks/`. Each task is atomic, individually
testable, and carries its `Tests` and `Gate` fields. For Small/Medium features this phase is
**skipped** — `sdd-implement` lists atomic steps inline instead.

## When this phase runs

- **Small/Medium**: skip. Tasks are implicit; `sdd-implement` lists atomic steps inline.
- **Large/Complex**: run. Produce the task index + detail files + coverage matrix.

## Steps

1. Load `sdd-context` for the feature. Require approved `spec.md` and (for Large/Complex) `design.md`.
2. **Test Coverage Matrix (always when this phase runs)**:
   - Scan the project for testing guidelines (AGENTS.md, CONTRIBUTING.md, test-runner config,
     CI workflows) and extract the real commands. Never invent commands or assume an ecosystem.
   - Sample 5-10 existing test files to infer layer coverage and location patterns (a floor, never
     a ceiling).
   - If no tests exist, ask the user which test types and commands to use.
   - Produce the matrix: per code layer — required test type, coverage expectation, location
     pattern, run command. Plus the Gate Check Commands table (Quick/Full/Build).
3. Delegate the breakdown to the `architect` subagent (read-only): dependency-ordered atomic tasks,
   each mapping to plan items and acceptance criteria. Tag each task by domain — `backend`,
   `react`, `vue`, `test`, `infra`.
4. Write the artifacts:
   - `specs/<feature>/tasks.md` — Test Coverage Matrix + Gate Check Commands + task index:
     ```
     # <Feature> — Tasks
     ## Test Coverage Matrix
     ## Gate Check Commands
     ## Task Breakdown
     - [ ] T01 - <slug> - backend
     - [ ] T02 - <slug> - react
     ```
   - `specs/<feature>/tasks/<task-id>-<slug>.md` — one file per task:
     ```
     # T01 - <slug>
     ## Status
     TODO
     ## Domain
     backend
     ## Depends on
     -
     ## Requirement
     AUTH-01
     ## Description
     ## Acceptance criteria
     ## Files likely touched
     app/Services/LoginService.php
     ## Tests
     unit
     ## Gate
     quick
     ```
   - **Test co-location**: every task that creates/modifies a testable layer includes writing those
     tests in the same task. "Tested in another task" is not a valid `Tests: none`.
5. **Pre-approval gate**: run `python3 <scripts-dir>/validate_tasks.py <feature>`. Non-zero exit
   means restructure before presenting.
6. Present the task list for human confirmation (approve, reorder, or trim).

## Test Coverage Matrix

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | -------------------- | ---------------- | ----------- |

Strong defaults when no guideline applies:

| Layer type | Strong default |
| ---------- | -------------- |
| Domain / business logic | All branches; 1:1 to spec ACs; every listed edge case has a test |
| Route / controller / e2e | Every route in scope: happy path + edge cases + error paths |
| Repository / data-access | Key query paths + error handling |
| Entity / config / schema | none — build gate only |

## Gate Check Commands

| Gate Level | When to Use | Command |
| ---------- | ----------- | ------- |
| Quick | After tasks with unit tests only | [unit command] |
| Full | After tasks with e2e/integration tests | [unit + e2e commands] |
| Build | After phase completion or config/entity-only tasks | [build + lint + all tests] |

## Definition of done

- Tasks are atomic (one deliverable: one component/function/endpoint/file change) and
  dependency-ordered via `Depends on`.
- Every task has `Tests` + `Gate` fields consistent with the Test Coverage Matrix.
- Every acceptance criterion has a covering task; every task maps to a requirement ID.
- Each task is implementable and testable in isolation.
- `python3 <scripts-dir>/validate_tasks.py <feature>` exits 0.
- The human approved the breakdown.

## Scripts

Validation scripts ship in the harness `scripts/` directory (installed as `.opencode/scripts/` in
the target project). Resolve them as `<skill-dir>/../../scripts/<name>.py`. Never run
`python3 scripts/...` from the consuming project root.