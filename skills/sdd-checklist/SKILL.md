---
name: sdd-checklist
description: Quality gate on a feature spec. Have the reviewer verify the spec is complete, precise (EARS), unambiguous, and consistent with the constitution and coding standards; use grilling to close gaps; write specs/<feature>/checklist.md. Run before planning large or ambiguous features.
---

## What I do

Check that the spec is *ready* before it is implemented on — the checklist is a set of
requirements-quality criteria, not an implementation tracker. Unchecked items mean the spec needs
tightening, not that code work is pending.

## Steps

1. Load `sdd-context` for the feature. Require `specs/<feature>/spec.md` to exist and pass
   `validate_spec.py`.
2. Delegate the evaluation to the `reviewer` subagent (read-only). Ask for a checklist covering:
   - Every user story has testable, **EARS-shaped** acceptance criteria (WHEN/WHILE/WHERE/IF or
     ubiquitous `The system SHALL ...`) with concrete values and a SHALL.
   - Every criterion has a single interpretation and a precise, spec-defined expected outcome —
     no criterion readable two ways.
   - Edge cases and invalid inputs are specified.
   - Non-goals (Out of Scope) are stated.
   - Terminology is unambiguous and consistent.
   - Every requirement maps to a `CATEGORY-NNN` ID in the traceability table.
   - The spec is consistent with `docs/scope.md`, `specs/constitution.md`, and the applicable
     `.coding-standards/` docs (paths referenced for the relevant stacks).
3. Write `specs/<feature>/checklist.md` with the reviewer's items as `[ ]`/`[x]`.
4. For every `[ ]` item, run `grilling` with the human to resolve the gap, then update the spec via
   the `sdd-spec` flow. Re-run this gate until the checklist is clean.

## Rules

- The checklist is reviewer-owned: `[x]` means the reviewer determined the requirement-quality
  criterion is satisfied — it does not mean implementation work is complete.
- Do not proceed to `sdd-tasks`/`sdd-implement` while meaningful `[ ]` items remain.

## Scripts

Validation scripts ship in the harness `scripts/` directory (installed as `.opencode/scripts/` in
the target project). Resolve them as `<skill-dir>/../../scripts/<name>.py`. Never run
`python3 scripts/...` from the consuming project root.