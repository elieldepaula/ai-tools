---
description: Resume a feature in progress
agent: sdd
subtask: false
---
Run the `sdd-resume` skill for the feature `$ARGUMENTS`.

Steps:
1. Load `sdd-context` for the feature (includes the repo topology — single-repo vs multirepo).
2. Read `specs/STATE.md` (`## Decisions` + `## Handoff`).
3. Reconcile the Handoff against git evidence (read-only) and `specs/<feature>/tasks.md` — evidence
   wins over a stale snapshot. In a `multirepo`, reconcile per repo; commits exist only if the human
   made them, so uncommitted work is the expected state.
4. Reconstruct the state (DONE markers, pending tasks, convergence gaps).
5. If nothing is pending, report the feature as converged and suggest review.
6. Otherwise continue with the next pending task via the `sdd-implement` flow.