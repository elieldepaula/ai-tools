---
description: Implement the tasks of a feature (inline or formal, auto-sized)
agent: sdd
subtask: false
---
Run the `sdd-implement` skill for the feature `$ARGUMENTS`.

Steps:
1. Load `sdd-context` for the feature. Read `specs/<feature>/tasks.md` and the `tasks/` files (or
   list atomic steps inline for Small/Medium — if >5 steps, stop and run `/sdd-tasks` instead).
   Note the repo topology from the context (`single-repo` vs `multirepo`) — it decides who commits.
2. Pick the next pending task/step (first not-DONE whose dependencies are DONE).
3. Delegate the task to the matching dev agent by domain: `backend` → `backend-dev`,
   `react` → `react-dev`, `vue` → `vue-dev`.
4. Run the task's gate check command (from the Test Coverage Matrix / Gate Check Commands).
5. Mark the task complete, validate the message with
   `python3 <scripts-dir>/check_commit.py --message "<msg>"`, then close the unit by topology:
   - `single-repo`: one atomic Conventional Commit per task (implementation + tests + status
     together; never batch tasks).
   - `multirepo`: do NOT commit. Append the change to a commit-ready handoff for the human
     (files changed per repo + suggested Conventional Commit message).
6. Delegate verification to the `tester` agent (read-only); send back for fixes if it fails.
7. After the LAST task, dispatch a fresh `verifier` agent (author != verifier) — see `/sdd-verify`
   and the `sdd-verify` skill. Never mark the feature done before the Verifier reports PASS and
   `validate_state.py` exits 0.