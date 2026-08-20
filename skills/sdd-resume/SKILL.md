---
name: sdd-resume
description: Resume a feature that is in progress. Read specs/<feature>/tasks.md, the tasks/ files, and specs/STATE.md (Handoff + Decisions); reconcile the Handoff against git evidence; then continue implementing the next pending task via sdd-implement. Use with a feature name.
---

## What I do

Re-establish where a feature stopped and continue from exactly that point. State lives in
`specs/<feature>/tasks.md` (index, with `DONE` markers), the per-task files under `tasks/`
(`## Status`), and `specs/STATE.md` (`## Handoff` + `## Decisions`). Resume never depends on
conversation history.

## Steps

1. Load `sdd-context` for the feature (includes active decisions, confirmed lessons, and the repo
   topology — `single-repo` vs `multirepo`).
2. Read `specs/STATE.md`:
   - `## Decisions` — re-confirm active constraints; nothing superseded since last session?
   - `## Handoff` — treat as a **hypothesis** (feature, phase/task, next step, blockers,
     uncommitted files, branch), not ground truth.
3. **Reconcile Handoff against git evidence** (read-only git — never write):
   - `single-repo`: current branch vs Handoff `Branch`; `git status --porcelain`; recent commits
     (messages and touched files); `tasks.md` completion marks. A task with a passing gate and an
     atomic commit already on the branch → do not redo it; mark it complete if still open, continue
     from the next incomplete task.
   - `multirepo`: reconcile per repo (each repo's `git status --porcelain` and `git log`). Commits
     exist only if the human made them — uncommitted work in the working tree is the **expected**
     state, so do not treat it as an anomaly. Rebuild the next step from `tasks.md` + the working
     tree, then propose it.
   - Partial unverified work in the working tree → preserve it, re-run the gate, then finish the
     status+commit cycle (`single-repo`) or prepare the commit-ready handoff (`multirepo`).
   - Stale or missing Handoff → rebuild next-step from git + `tasks.md`, then propose that.
   - Unexplained local changes you cannot map to the current task → STOP and ask; do not discard.
4. Read `specs/<feature>/tasks.md` and every `tasks/<id>-<slug>.md`. Build the state:
   - DONE tasks; the next pending task (first not-DONE whose dependencies are DONE).
   - Any `## Convergence` gap tasks appended by `sdd-converge`.
5. If nothing is pending, report the feature as converged and suggest the human review.
6. Otherwise hand the state to the `sdd-implement` flow and resume with the next pending task.
7. If artifacts are inconsistent (e.g., a DONE task whose status file is missing), repair the
   artifacts to match reality before proceeding, and flag it to the human.
8. **Update the Handoff** (section-scoped write — never clobber `## Decisions`) with the reconciled
   state and proposed next step before beginning work.

## Definition of done

The feature's exact state is reconstructed from disk + git, reconciled against the Handoff, and
implementation resumes at the correct task with no guesswork from memory.

## Coding standards

- Re-load the applicable `.coding-standards/` docs when resuming so implementation continues against
  the same standards.