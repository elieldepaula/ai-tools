---
name: sdd-converge
description: Final verification that an implemented feature satisfies its spec, plan, and tasks. Runs the deterministic completion gate (validate_state.py), distills lessons from grounded failures (lessons.py), and appends gap tasks when something is missing. Repeat until converged. Use after sdd-implement.
---

## What I do

Confirm nothing was missed. After the Verifier reports PASS, the deterministic gate confirms the
report is real, and grounded failures become reusable lessons. This phase is append-only: it never
edits or deletes code; its only possible write is adding tasks to `tasks.md`.

## Steps

1. Load `sdd-context` for the feature. Require `sdd-implement` (and the Verifier) to have completed.
2. **Deterministic completion gate**: run `python3 <scripts-dir>/validate_state.py <feature>`.
   - Non-zero exit = the feature is NOT done: `specs/<feature>/validation.md` is missing, unfilled,
     FAIL, or lacks `file:line` evidence. Route the FAIL gaps to fix tasks and re-verify.
3. Have the `reviewer` subagent (read-only) cross-check the codebase against spec, plan, and tasks —
   severity-graded findings summary.
4. **Distill lessons**: for each grounded failure (surviving mutant, spec-precision gap, failed AC,
   SPEC_DEVIATION) run:
   `python3 <scripts-dir>/lessons.py add --feature <feature> --signal <signal> --source <file:line> --text "<terse lesson>"`
   A clean PASS records nothing. If there was signal but no lesson was recorded, say so in chat.
5. Outcomes:
   - **Converged** — no gaps. Report the clean result and recommend the human review and ship.
   - **Gaps found** — append the gaps as new tasks under a `## Convergence` section in `tasks.md`
     (index + `tasks/` detail files), then run `sdd-implement` again and re-run `sdd-converge`.
     Each pass finds fewer items; repeat until converged.

## Definition of done

- `python3 <scripts-dir>/validate_state.py <feature>` exits 0 (real PASS report with evidence).
- No open gaps remain, or the remaining gaps are tracked as tasks and being implemented.
- Lessons distilled for every grounded failure.

## Scripts

Validation scripts ship in the harness `scripts/` directory (installed as `.opencode/scripts/` in
the target project). Resolve them as `<skill-dir>/../../scripts/<name>.py`. Never run
`python3 scripts/...` from the consuming project root.