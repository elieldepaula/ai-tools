---
name: sdd-implement
description: Execute the tasks of a feature in dependency order, auto-sized to the feature's tier. Lists atomic steps inline when tasks are implicit (Small/Medium) or executes the formal task breakdown (Large/Complex). Delegates each task to the correct dev agent, enforces atomic Conventional Commits (check_commit.py), and dispatches the independent Verifier after the last task. Use with a feature name and optionally a task id.
---

## What I do

Implement the pending work of `specs/<feature>/` one unit at a time, in dependency order, verifying
each before moving on. A task/step is DONE only when implemented, verified, and — in a `single-repo`
— committed; in a `multirepo` the changes are prepared for the human to commit.

## Auto-sizing

- **Small/Medium (no tasks.md):** list atomic steps inline before writing any code. Each step is
  one deliverable, independently verifiable and committable. If the listing reveals >5 steps or
  complex dependencies, STOP and run `sdd-tasks` — the tasks phase was wrongly skipped.
- **Large/Complex (tasks.md exists):** execute the formal task breakdown in dependency order.

## Steps

1. Load `sdd-context` for the feature. Read `specs/<feature>/tasks.md` (if present) or the inline
   plan, and the `tasks/` files. Note the repo topology from the context (`single-repo` vs
   `multirepo`) — it decides who commits.
2. Determine the next unit: first not-DONE task whose dependencies are DONE (or the next inline
   step). If a task id was given, start there (respecting dependencies).
3. Delegate the task to the matching dev agent by its `Domain` tag:
   - `backend` → `backend-dev`, `react` → `react-dev`, `vue` → `vue-dev`
   - mixed → split or pick by stack declared in `AGENTS.md`
   The dev agent returns the implementation and its own test results.
4. **Gate check (deterministic, non-negotiable):** run the task's Gate command (from the coverage
   matrix). The test runner decides correctness, not self-assessment. Non-zero exit = fix, re-run.
5. **Close the unit by topology:**
   - `single-repo` — mark the task complete in `tasks.md` (or the inline plan), validate the
     message with `python3 <scripts-dir>/check_commit.py --message "<msg>"` (Conventional
     Commits), then make **one atomic commit per task**: implementation + tests + status updates
     together. Never batch tasks.
   - `multirepo` — mark the task complete in `tasks.md` (or the inline plan), validate the
     proposed message with `python3 <scripts-dir>/check_commit.py --message "<msg>"`, then **do
     not commit**. Append the change to a commit-ready handoff for the human: per repo, the files
     changed and the suggested Conventional Commit message. Never run `git add`/`commit` or any
     other git write command.
6. Verify with the `tester` subagent (read-only) when a broader check is needed: focused tests,
   then the broader suite and lint. If verification fails, send back to the dev agent, re-verify.
7. Repeat for the next task/step until all are done.

## After the last task: Verifier (MANDATORY, never prompted)

Dispatch a fresh `verifier` subagent (author != verifier) — see `sdd-verify`. It runs the
spec-anchored coverage check and the lightweight discrimination sensor, writes
`specs/<feature>/validation.md`, and returns a PASS/FAIL verdict. Fix→re-verify is bounded to 3
iterations before escalating to the user.

## Rules

- Never mark a task DONE without passing its gate check.
- Never weaken, delete, or skip tests to make them pass. Tests are the spec.
- Never skip dependency ordering; never parallelize dependent tasks.
- In a `multirepo`, never run git write commands — no `add`, `commit`, `branch`, `checkout`,
  `push`, `pull`, `merge`, `stash`, `rebase`, `reset`, `tag`, or `worktree`. The human commits.
- If a task reveals a spec/plan gap, stop and go back to `sdd-spec`/`sdd-plan`.
- A task is not done until the Verifier reports PASS and `validate_state.py` exits 0.

## Coding standards

- The dev agents apply the coding standards referenced in their agent definitions and in each
  task's `## Tests`/`## Gate` — docs under `.coding-standards/`.
- The tester verifies implemented code against these standards. If a doc is missing, fall back to
  `AGENTS.md` and flag it.

## Scripts

Validation scripts ship in the harness `scripts/` directory (installed as `.opencode/scripts/` in
the target project). Resolve them as `<skill-dir>/../../scripts/<name>.py`. Never run
`python3 scripts/...` from the consuming project root.