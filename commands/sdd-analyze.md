---
description: Cross-artifact consistency analysis (spec, design, tasks) incl. traceability
agent: sdd
subtask: false
---
Run the `sdd-analyze` skill for the feature `$ARGUMENTS`.

Steps:
1. Load `sdd-context` for the feature. Require `spec.md` (and `design.md`/`tasks.md` if present).
2. Delegate the consistency analysis to the `reviewer` agent (read-only): conflicts, gaps, and
   ambiguities across the artifacts, severity-graded, plus requirement traceability gaps and
   coding-standard coverage.
3. Present the report to the human with recommended remediations.
4. Loop back to the owning phase (`sdd-spec`, `sdd-plan`, or `sdd-tasks`) for each finding, then
   re-run this analysis until clean. Never patch the artifacts to silence a finding.