# Tasks — <Feature Name>

**Feature status:** DRAFT | SPECIFICATION | ARCHITECTURE | READY | IN PROGRESS | VALIDATION | REVIEW | DONE

**Spec:** specs/<feature-id>/spec.md
**Acceptance:** specs/<feature-id>/acceptance.md
**Architecture:** specs/<feature-id>/architecture.md

> **Convention (mandatory):** this file is the canonical index — IDs, titles, dependencies, status, links only. No Task bodies inline. Every Task has its own file at `tasks/<TASK-ID>-<slug>.md` (slug in kebab-case) with the detailed Task specification.

## Index

| ID | Title | Depends on | Status | Detail |
| -- | ----- | ---------- | ------ | ------ |
| TASK-001 | <title> | — | PENDING | [tasks/TASK-001-<slug>.md](tasks/TASK-001-<slug>.md) |
| TASK-002 | <title> | TASK-001 | PENDING | [tasks/TASK-002-<slug>.md](tasks/TASK-002-<slug>.md) |

## Dependencies (overview)

```text
TASK-001 → TASK-002 → ...
```
