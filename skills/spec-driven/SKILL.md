---
name: spec-driven
description: Specification-driven software development workflow for AI agents. Use when starting projects or features, decomposing ambiguous or complex requirements, creating implementation tasks, validating work against a specification, or coordinating multi-agent development. Do not use for trivial one-line changes, typo fixes, or formatting-only changes.
---

# Spec-Driven Development

The specification is the source of truth for behavior. Meaningful changes are driven by explicit, version-controlled specs — not isolated prompts or undocumented assumptions.

Technology-agnostic: framework-specific rules come from other skills.

## Activation checklist

When this skill applies:

1. **Classify size** using [Size tiers](#size-tiers). Skip the skill if trivial.
2. **Inspect the repo** for existing specs, architecture, tests, and related code.
3. **Resolve ambiguity** — facts from the repo; business decisions via the `grilling` skill. Do not invent business rules.
4. **Write or update** files under `specs/<feature-id>/` (use [templates/](templates/)).
5. **Capture** any explicit requirement from chat into the spec before implementing.
6. **Decompose** into Tasks when the Feature cannot be one isolated change.
7. **Implement one Task at a time**, loading context in order (below).
8. **Validate** against acceptance criteria and the Feature spec; emit a [completion report](#completion-report).

## When to use / skip

| Use | Skip |
| --- | ---- |
| New project, Epic, Feature, or capability | Typo / comment / formatting-only fixes |
| Ambiguous or incomplete requirements | Rename with no behavioral impact |
| Multiple components, layers, or integrations | Trivial, fully explicit one-step change |
| Business rules, API/DB/async changes | Mechanical dependency bump with no design choice |
| Multi-agent or multi-Task work | |
| Need explicit acceptance criteria or validation against a contract | |

When unsure: prefer the skill if misunderstanding the requirement costs more than writing a short spec.

## Size tiers

Introduce only the structure the work justifies:

| Size | Artifacts |
| ---- | --------- |
| **Small** | Thin `spec.md` + `acceptance.md` + one Task (`tasks/TASK-001-<slug>.md`) |
| **Medium** | Above + `architecture.md` + full `tasks.md` with dependencies |
| **Large** | Above + Epic nesting, ADRs, dependency graph, multi-agent parallel Tasks |

## Repository layout

```text
specs/
└── <feature-id>/          # slug, or COM-102-order-splitting when linked to PM tools
    ├── spec.md
    ├── architecture.md    # Medium+
    ├── acceptance.md
    ├── tasks.md           # Canonical index (IDs, titles, deps, status, links) — no inline bodies
    ├── tasks/             # One file per Task, <TASK-ID>-<slug>.md
    │   └── TASK-001-core-scaffold.md
    └── adr/               # Large / significant decisions
        └── ADR-001.md
```

Optional Epic nesting: `specs/<epic-id>/<feature-id>/`.

**Convention (mandatory):** `tasks.md` is the canonical index and contains **only** IDs, titles, dependencies, status, and links — never inline Task bodies. Every Task gets its own file at `tasks/<TASK-ID>-<slug>.md` (slug in kebab-case, e.g. `TASK-001-core-scaffold.md`) holding the detailed Task specification: Scope, Requirements, Dependencies, Acceptance Criteria, and Expected Tests. One Task per file; one file per Task.

Copy starters from [templates/](templates/). See [reference.md](reference.md) for hierarchy, lifecycle, and Jira/Kanban mapping.

## Spec vs architecture vs implementation

| Layer | Answers | Lives in |
| ----- | ------- | -------- |
| **Spec** | What behavior / rules / scope / out-of-scope | `spec.md` |
| **Acceptance** | Objectively testable scenarios | `acceptance.md` |
| **Architecture** | How it fits the system | `architecture.md` |
| **Task** | One implementable unit referencing the Feature | `tasks/` (one file per Task) |
| **ADR** | Significant technical decision | `adr/` |

Prefer behavior in the spec:

```text
The customer can only add products belonging to the same collection to a quote.
```

Not implementation detail (that belongs in architecture/Task):

```text
Create an around plugin on Magento\Quote\Model\Quote.
```

A Feature is a capability; a Task is an implementation unit. `Feature != Task`.

## Ambiguity

```text
Requirement → inspect repo
  ├─ answerable from code/docs/specs/tests → resolve there
  └─ business decision / conflict / missing acceptance → grilling
       → capture decision in spec + acceptance + affected Tasks
       → then continue
```

Use `grilling` for business behavior, edge cases, conflicts, scope, constraints, integrations, data ownership, compatibility, security/performance — not for facts you can look up.

## Context loading (before implementing a Task)

```text
Project rules → relevant skills → Epic (if any) → Feature spec →
architecture → acceptance → Task → existing code → tests
```

Load only what the Task needs.

## Source of truth (conflicts)

```text
Explicit current requirement (must be written into the spec before continuing)
  → Feature specification
  → Architecture
  → Project rules
  → Existing implementation
  → Agent assumption (never silently invent business rules)
```

**Explicit current requirement** means a clear instruction from the human in this session (or a linked ticket the human pointed at). If it contradicts architecture or project rules, surface the conflict — do not silently override.

## Relationship to planning-with-files

| Artifact | Role |
| -------- | ---- |
| `specs/<feature-id>/` | Durable contract: versioned with the codebase |
| `task_plan.md` / `findings.md` / `progress.md` | Session working memory for multi-step execution |

Use **spec-driven** for what to build and how to know it is done. Use **planning-with-files** to track phases and progress while executing Tasks. Do not treat planning files as a substitute for the Feature specification.

## Agent responsibilities (per Task)

1. Read Feature spec, relevant architecture, and the Task.
2. Inspect codebase and conventions; stay in scope.
3. Implement; add/update tests; run relevant tests.
4. Validate against acceptance criteria and the Feature spec.
5. Report deviations, assumptions, and unresolved questions.

Do not treat the Task text as complete context — the Feature spec remains authoritative.

## Implementation rules

- Minimize changes outside Task scope; prefer the smallest implementation that satisfies the spec.
- Reuse existing abstractions; avoid speculative ones and unnecessary dependencies.
- Preserve backward compatibility unless the spec says otherwise.
- Follow project coding standards; keep architectural boundaries.
- Do not change public APIs without authorization; do not modify unrelated features.
- Do not weaken tests to pass a wrong implementation — if a test conflicts with the new spec, call it out.

## Completion report

Before declaring a Task complete, validate: implementation → unit/integration tests → acceptance → specification (and architecture when present).

```text
Task: <id>
Status: COMPLETE | BLOCKED | PARTIAL
Implementation: <summary>
Files Changed: <list>
Tests: <executed>
Acceptance Criteria: PASS | PARTIAL | FAIL
Specification: PASS | PARTIAL | FAIL
Architecture: PASS | PARTIAL | FAIL | N/A
Assumptions: <list>
Remaining Issues: <list>
```

Never mark COMPLETE if required validation was skipped. Feature done only when all required Tasks, tests, acceptance, spec, architecture (if any), and review are satisfied — not merely because cards are marked done.

## Spec changes mid-implementation

If implementation shows the spec is wrong or incomplete: update the spec → review impact → update Tasks/acceptance → notify the human when scope changes materially → continue. Do not bury behavior changes only in code.

## Additional resources

- [reference.md](reference.md) — hierarchy, lifecycle, Jira/Kanban, multi-agent roles, important rules
- [examples.md](examples.md) — end-to-end Feature walkthrough
- [templates/](templates/) — `spec.md`, `architecture.md`, `acceptance.md`, `tasks.md`, `task.md`, `adr.md`
