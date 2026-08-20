---
description: Break a feature plan into tasks (Large/Complex only)
agent: sdd
subtask: false
---
Run the `sdd-tasks` skill for the feature `$ARGUMENTS`.

Steps:
1. Load `sdd-context` for the feature. Require approved `spec.md` and (for Large/Complex) `design.md`.
2. Generate the Test Coverage Matrix and Gate Check Commands from the codebase (guidelines + sample
   test files + real commands) and include them in `tasks.md`.
3. Delegate the breakdown to the `architect` agent (read-only): dependency-ordered atomic tasks
   tagged by domain (`backend`, `react`, `vue`, `test`, `infra`), each mapping to requirement IDs,
   with `Tests` + `Gate` fields (test co-located per task).
4. Write `specs/<feature>/tasks.md` (matrix + index) and `specs/<feature>/tasks/<task-id>-<slug>.md`
   (one detailed file per task).
5. Run the pre-approval gate: `python3 <scripts-dir>/validate_tasks.py <feature>` — fix until it
   exits 0.
6. Present the task list for human confirmation before proceeding to `/sdd-implement <feature>`.

Note: for Small/Medium features this phase is skipped — tasks are implicit and listed inline by
`/sdd-implement`.