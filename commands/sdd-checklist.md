---
description: Quality gate on a feature spec
agent: sdd
subtask: false
---
Run the `sdd-checklist` skill for the feature `$ARGUMENTS`.

Steps:
1. Load `sdd-context` for the feature. Require `specs/<feature>/spec.md` to exist and pass
   `validate_spec.py`.
2. Delegate the evaluation to the `reviewer` agent (read-only): completeness, clarity, EARS
   precision, unambiguity, traceability, and consistency with the constitution and coding standards.
3. Write `specs/<feature>/checklist.md` with the reviewer's `[ ]`/`[x]` items.
4. Use the `grilling` skill to close every `[ ]` gap with the human, update the spec via the
   `sdd-spec` flow, and re-run this gate until clean.