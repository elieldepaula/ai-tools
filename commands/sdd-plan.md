---
description: Create the technical plan/design for a feature (Large/Complex only)
agent: sdd
subtask: false
---
Run the `sdd-plan` skill for the feature `$ARGUMENTS`.

Steps:
1. Load `sdd-context` for the feature. Require an approved `specs/<feature>/spec.md`.
2. Read active decisions from `specs/STATE.md` (`## Decisions`); conform or supersede — never ignore.
3. Delegate the design to the `architect` agent (read-only): architecture, data contracts, backend
   and frontend changes, migrations, risks — grounded in `AGENTS.md` and `.coding-standards/`.
4. Use the `grilling` skill to resolve open design decisions with the human.
5. Write `specs/<feature>/design.md` following the skill's format.
6. Record project-level decisions as new `AD-NNN` entries in `specs/STATE.md`.
7. Present the design for human approval before proceeding to `/sdd-tasks <feature>`.

Note: for Small/Medium features this phase is skipped — design happens inline during
implementation.