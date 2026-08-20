---
description: Show the assembled SDD project context
agent: sdd
subtask: false
---
Run the `sdd-context` skill to assemble and display the current project context for the SDD workflow.

Include: the stack from `AGENTS.md`, the test commands, the repo topology from `AGENTS.md` `## Git`
(single-repo vs multirepo — decides who owns git), the relevant principles from
`specs/constitution.md`, active project decisions from `specs/STATE.md`, confirmed lessons from the
lessons store, a summary of the applicable `.coding-standards/` docs, a summary of `docs/scope.md`,
and — if a feature name was given as argument `$ARGUMENTS` — the current state of `specs/<feature>/`
(spec/design/tasks and their progress).