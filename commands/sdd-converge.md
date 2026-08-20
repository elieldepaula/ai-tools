---
description: Final convergence check on an implemented feature (completion gate + lessons)
agent: sdd
subtask: false
---
Run the `sdd-converge` skill for the feature `$ARGUMENTS`.

Steps:
1. Load `sdd-context` for the feature. Require `sdd-implement` (and the Verifier) to have completed.
2. Run the deterministic completion gate: `python3 <scripts-dir>/validate_state.py <feature>` —
   non-zero exit means the feature is NOT done (fix gaps and re-verify).
3. Delegate the verification to the `reviewer` agent (read-only): check the codebase against every
   acceptance criterion, plan item, and task; severity-graded findings.
4. Distill lessons for grounded failures via
   `python3 <scripts-dir>/lessons.py add --feature <feature> --signal <signal> --source <file:line> --text "<terse lesson>"`.
5. If gaps exist, append them as new tasks under a `## Convergence` section in `tasks.md`, run
   `/sdd-implement <feature>` again, and re-run converge until it reports clean.