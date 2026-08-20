---
name: sdd-plan
description: Produce the technical plan for a feature (the how) — only for Large/Complex features. Delegates design to the architect, records project-level decisions in specs/STATE.md, and produces specs/<feature>/design.md grounded in the stack declared in AGENTS.md. Skip this phase for Small/Medium features (design happens inline). Use with a feature name.
---

## What I do

Produce the "how" for Large/Complex features: architecture, components, data contracts,
integration steps. For Small/Medium features this phase is **skipped** — design is captured inline
during implementation. This phase also maintains the project decision log.

## When this phase runs

- **Small/Medium**: skip. Implementation carries design decisions inline.
- **Large/Complex**: run. Produce `specs/<feature>/design.md` and record project-level decisions.

## Steps

1. Load `sdd-context` for the feature. Require an approved `specs/<feature>/spec.md`.
2. **Read active decisions** from `specs/STATE.md` (`## Decisions`). Every `active` `AD-NNN` is a
   project-level constraint the design must conform to. Conform or supersede (append a new `AD-NNN`
   with the old one marked `superseded by AD-NNN`) — never silently ignore.
3. **Load confirmed lessons** relevant to the feature (`lessons.py list --status confirmed
   [--scope]`). Apply as guidance; never invent requirements.
4. **Research** (Complex features, or unfamiliar technology): follow the knowledge verification
   chain — codebase → project docs → web → flag as uncertain. Never fabricate APIs or patterns.
5. Delegate the design to the `architect` subagent (read-only): architecture, data contracts,
   module/component breakdown for Laravel + the relevant frontend, migrations/integration steps,
   risks, and code-reuse analysis. Ground in `AGENTS.md` and `.coding-standards/`.
6. Review the design. Run `grilling` to resolve open design decisions (package choices, data model)
   with the human — technical decisions are the human's, not yours.
7. Write `specs/<feature>/design.md` in the format below.
8. **Record project-level decisions**: any decision here that future features must follow goes to
   `specs/STATE.md` `## Decisions` as the next `AD-NNN` (append-only). Feature-local decisions stay
   in the design doc's Tech Decisions table.
9. Present the design for human approval before proceeding to `sdd-tasks`.

## Design format

```markdown
# <Feature> — Design

## Architecture Overview
(mermaid diagram where helpful)

## Code Reuse Analysis
### Existing Components to Leverage
| Component | Location | How to Use |
### Integration Points
| System | Integration Method |

## Components
### <Component>
- Purpose / Location / Interfaces / Dependencies / Reuses

## Data Models
### <Model>
(schema + relationships)

## Error Handling Strategy
| Error Scenario | Handling | User Impact |

## Risks & Concerns
| Concern | Location (file:line) | Impact | Mitigation |

## Tech Decisions
| Decision | Choice | Rationale |

## Test strategy
```

## Coding standards

- Ground design decisions in `.coding-standards/` — reference the relevant docs by path
  (e.g. `.coding-standards/Clean-Architecture.md`, `.coding-standards/SOLID.md`,
  `.coding-standards/PSR-12.md`, `.coding-standards/Laravel.md`, `.coding-standards/React.md`,
  `.coding-standards/Vue.md`) so implementers and reviewers load the same source.
- If a referenced doc is missing, fall back to the stack in `AGENTS.md` and flag it.

## Definition of done

- Every spec requirement maps to a concrete design item.
- Design conforms to (or explicitly supersedes) every active `AD-NNN` decision.
- Project-level decisions are recorded in `specs/STATE.md`.
- Stack decisions reference `AGENTS.md` and the applicable `.coding-standards/` docs.
- The human has approved the design.