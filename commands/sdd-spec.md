---
description: Create or update the specification for a feature (auto-sized by complexity)
agent: sdd
subtask: false
---
Run the `sdd-spec` skill for the feature `$ARGUMENTS`.

Steps:
1. Load `sdd-context` for the feature (includes active decisions + confirmed lessons).
2. Assess the feature scope (Small/Medium/Large/Complex) and confirm the tier with the human.
3. Delegate the spec analysis to the `architect` agent (read-only): problem statement, goals,
   user stories, EARS-shaped acceptance criteria, edge cases, out-of-scope, assumptions,
   requirement traceability, success criteria.
4. For Large/Complex (or when gray areas / implicit-requirement dimensions exist), use the
   `grilling` skill to resolve every open question with the human.
5. Write `specs/<feature>/spec.md` following the skill's format.
6. Run the closure gate: `python3 <scripts-dir>/validate_spec.py <feature>` — fix until it exits 0.
7. Present the spec for human approval before proceeding to the next phase for the tier
   (`/sdd-plan` or `/sdd-tasks` for Large/Complex; `/sdd-implement` directly for Small/Medium).