# Spec-Driven Reference

Supporting detail for the `spec-driven` skill. Read when you need hierarchy, lifecycle, PM-tool mapping, or multi-agent role mapping.

## Hierarchy

```text
EPIC (large business objective — why the work exists)
└── FEATURE (concrete capability)
    ├── SPEC (behavior)
    ├── ARCHITECTURE (how it fits the system)
    ├── ACCEPTANCE CRITERIA (testable scenarios)
    └── TASKS (implementation units)
```

Not every request needs every level. Scale with size tiers in `SKILL.md`.

### Epic

Large product objective. Examples: Unified B2B Commerce, Payment Platform Migration.

### Feature

Concrete functional capability. Examples: Order Splitting, Shared Catalog Resolution.

### Tasks

Independently understandable, implementable, testable, reasonably small, tied to the Feature, explicit about dependencies. Do not redefine the Feature — reference the relevant spec section.

Task ids are project-defined: `TASK-001` or external ids (`COM-103`).

### Dependency graph

Model dependencies when order matters. Independent Tasks may run in parallel. Do not start a Task before its required dependencies are done.

```text
TASK-001 Quote Partitioning
      │
      ▼
TASK-002 Order Creation
      ├───────────────┐
      ▼               ▼
TASK-003           TASK-004
Payment            Invoice
      └───────┬───────┘
              ▼
          TASK-005 Integration Tests
```

## Spec checklist

A Feature specification should answer:

1. What problem does it solve?
2. What business behavior is required?
3. What are the business rules?
4. What inputs/outputs?
5. What invariants?
6. Exceptional situations?
7. Explicitly out of scope?
8. Acceptance criteria (in `acceptance.md`)?
9. Architectural constraints?

Omit sections that add no value.

## Acceptance criteria

Prefer scenario-oriented, testable criteria (Given/When/Then). Avoid vague quality statements ("should be clean"). Prefer invariants ("quote must never contain products from different collections").

## Tests as evidence

```text
Specification → Acceptance Criteria → Tests → Implementation
```

Cover normal behavior, business rules, invariants, edge cases, failures, regressions.

## Feature lifecycle

| State | Meaning |
| ----- | ------- |
| DRAFT | Idea or raw requirement |
| SPECIFICATION | Defining business behavior |
| ARCHITECTURE | Defining technical solution |
| READY | Specced enough to decompose into Tasks |
| IN PROGRESS | At least one Task underway |
| VALIDATION | Checking implementation against spec |
| REVIEW | Code/behavior review |
| DONE | Acceptance criteria satisfied |

Record status in `tasks.md` (Feature-level status line + per-Task status). Agents update status when they transition; do not invent a separate status store unless the project already has one.

## Jira / Kanban integration

PM tools are a management layer (priority, ownership, workflow). The repository holds the technical source of truth under `specs/`.

Link with stable ids:

```text
JIRA: COM-102  →  specs/COM-102-order-splitting/
Tasks: COM-103 … may match ticket ids
```

Recommended PM hierarchy: Epic → Feature → Tasks. Do not create an Epic per technical Task. The repo must remain usable if the PM tool is down.

## Multi-agent roles (this stack)

The main agent orchestrates; subagents do focused work and return reports. Select subagents by detected stack prefix (`magento-`, `laravel-`, `php-`, `react-`, `vue-`) + role suffix (`-architect`, `-developer`, `-qa`, `-reviewer`). Delegate by size tier (see `SKILL.md`): Small = inline; Medium+ = architect + qa + reviewer; Large = also parallel developers.

| Role | Typical agent | Responsibility | Delegation trigger |
| ---- | ------------- | -------------- | ------------------ |
| Spec / architecture | `*-architect` | Spec, acceptance, architecture, ADRs, Task decomposition | Size Medium or Large, before writing `specs/<feature-id>/` artifacts |
| Implementation | `*-developer` | One Task at a time within scope; follow architect decisions | Size Large, one agent per Task, parallel when independent |
| Tests / validation | `*-qa` | Test plan, execution evidence; never fixes code — reports to the developer | After implementation, before completion report |
| Review | `*-reviewer` | Spec + architecture + code review (readonly); hands findings to the developer | Before Feature DONE |

Imperative flow:

1. Main agent resolves ambiguity via `grilling` — facts from the repo; business decisions from the user. Never invent business rules.
2. **Medium or Large**: delegate spec + acceptance + architecture + ADRs + Task decomposition to the `*-architect`. The architect writes everything; the main agent does not.
3. **Large**: delegate each Task to a `*-developer` (independent Tasks in parallel). The developer returns implementation, tests, and a completion report.
4. Delegate test plan and execution to the `*-qa`. QA reports failures and bugs to the `*-developer` with reproduction steps — it never fixes code.
5. Before Feature DONE, delegate a readonly review to the `*-reviewer` against the spec and the project coding standards; route findings back to the `*-developer`.

Fallback: if no matching subagent exists, the main agent performs the stage inline rather than blocking the workflow.

## Architectural decisions

Significant decisions go in `specs/<feature-id>/adr/ADR-NNN.md` (context, decision, alternatives, consequences) so agents do not rediscover them.

## Important rules

1. **Specification first** — Do not implement a non-trivial Feature without understanding its spec.
2. **Feature ≠ Task** — Capability vs implementation unit.
3. **Spec ≠ implementation** — Behavior vs technical solution.
4. **Tests are evidence** — They verify the spec; they do not replace it.
5. **PM tools ≠ technical source of truth** — They reference repo specs.
6. **Do not invent business rules** — Use `grilling` when ambiguous.
7. **Validate against the specification** — Passing tests alone is not Feature complete.
8. **Keep changes scoped** — Do not modify unrelated functionality.
9. **Make dependencies explicit**.
10. **Keep specifications versioned** with the codebase.
11. **Scale process to the work**.
