---
description: Independent verification of an implemented feature (spec-anchored + discrimination sensor)
agent: sdd
subtask: false
---
Run the `sdd-verify` skill for the feature `$ARGUMENTS`.

Steps:
1. Load `sdd-context` for the feature. Confirm all tasks are implemented and committed.
2. Dispatch a fresh `verifier` agent (read-only, author != verifier) with the spec, the git diff
   surface, and the test files in scope.
3. The Verifier runs the spec-anchored coverage check and the lightweight discrimination sensor,
   then writes `specs/<feature>/validation.md` and returns a compact PASS/FAIL verdict.
4. On FAIL: route ranked gaps to fix tasks, re-verify (max 3 iterations, then escalate).
5. On PASS: run `python3 <scripts-dir>/validate_state.py <feature>` — non-zero exit means the
   feature is NOT done.
6. Distill lessons for grounded failures via `lessons.py add` (see `/sdd-converge`).