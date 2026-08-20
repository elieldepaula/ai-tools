---
name: sdd-spec
description: Create or update the specification for a feature (the what/why), auto-sized by complexity. Assesses scope (Small/Medium/Large/Complex), triggers grilling for ambiguity and the implicit-requirement dimensions sweep, and produces specs/<feature>/spec.md with EARS-shaped acceptance criteria and requirement IDs. Runs the deterministic closure gate (validate_spec.py) before human approval. Use with a feature name.
---

## What I do

Produce `specs/<feature>/spec.md` — the "what" and "why": problem statement, goals, user stories,
EARS-shaped acceptance criteria, edge cases, non-goals, assumptions, requirement traceability, and
success criteria. The complexity of the feature decides how deep this phase goes (auto-sizing).

## Auto-sizing

Assess the feature scope first and pick a tier. Present the tier to the user for confirmation.

| Tier | Scope signal | Specify depth | Next phases |
| ---- | ------------ | ------------- | ----------- |
| Small | ≤3 files, one sentence, no ambiguity | One-liner spec (inline) | Skip design/tasks; implement + verify |
| Medium | Clear feature, <10 tasks, no gray areas | Brief spec, no requirement IDs | Skip design/tasks; tasks implicit |
| Large | Multi-component feature | Full spec + requirement IDs | design + full tasks |
| Complex | Ambiguity, new domain, implicit-requirement dimensions present | Full spec + discuss gray areas + requirement IDs | design + research + phase plan |

**Discuss trigger:** if the feature has any implicit-requirement dimension (persistence/state,
external calls, auth, payments, concurrency, state transitions) or visible gray areas, run
`grilling` before locking the spec. Never guess on user-facing behavior.

## Steps

1. Load `sdd-context` for the feature. It includes the confirmed lessons (load only `confirmed`,
   via `lessons.py list --status confirmed`) and the active project decisions.
2. **Scope assessment**: classify the feature (Small/Medium/Large/Complex) from the request and a
   lightweight codebase scan. Confirm with the user.
3. **Clarify requirements** (thinking partner, not interviewer): ask open questions, challenge
   vagueness. Facts come from the environment (codebase/docs) — you look those up, you never ask.
   Run the **implicit-requirement dimensions sweep** for Large/Complex: every dimension resolves to
   a requirement or an explicit `N/A because ...`. Medium: cover only present dimensions. Small:
   skip.
4. **Discuss gray areas** (Large/Complex, or on trigger): use `grilling` to resolve every open
   question with the human. Declined gray areas become assumptions — never silently dropped.
5. **Write `specs/<feature>/spec.md`** in the format below. Acceptance criteria in EARS, one
   requirement per criterion, concrete values, every criterion has a SHALL. Assign requirement IDs
   (`CATEGORY-NNN`).
6. **Closure gate before presenting**:
   - Every AC has a single interpretation and a precise, spec-defined expected outcome. Split or
     log as an assumption otherwise.
   - Every open question is resolved or assumption-logged. Nothing proceeds unmarked.
   - **Deterministic backing**: run `python3 <scripts-dir>/validate_spec.py <feature>`. Non-zero
     exit means fix before presenting.
7. Present the spec for human approval before proceeding to `sdd-plan`/`sdd-tasks`/`sdd-implement`
   (whatever the tier dictates).

## Spec format

```markdown
# <Feature> — Spec

## Problem Statement
## Goals
- [ ] Goal with measurable outcome
## Out of Scope
| Feature | Reason |
## Assumptions & Open Questions
| Assumption / decision | Chosen default | Rationale | Confirmed? |
**Open questions:** none

## User Stories
### P1: <title> (MVP)
As a <role>, I want <capability> so that <benefit>.
### P2: <title>
### P3: <title>

## Acceptance Criteria
1. WHEN <trigger> THEN the system SHALL <response>      <!-- event-driven -->
2. IF <undesired condition> THEN the system SHALL <response>  <!-- unwanted-behavior -->
3. WHILE <state> the system SHALL <response>            <!-- state-driven -->
4. WHERE <feature present> the system SHALL <response>  <!-- optional-feature -->
5. The system SHALL <always-on invariant>               <!-- ubiquitous -->

## Edge Cases
## Requirement Traceability
| Requirement ID | Story | Phase | Status |
| AUTH-01 | P1 | Design | Pending |
## Success Criteria
- [ ] Measurable outcome
## Definition of done
```

**EARS patterns:** each criterion resolves to exactly one pattern (WHEN/WHILE/WHERE/IF or
ubiquitous `The system SHALL ...`). Failure states, state transitions, and optional behavior are
first-class criteria, not footnotes. If you cannot write a criterion as a test, rewrite it.

## Definition of done

- Every user story has testable, EARS-shaped acceptance criteria with concrete values and a SHALL.
- Every requirement maps to a `CATEGORY-NNN` ID in the traceability table.
- Every open question and every implicit-requirement dimension is resolved or assumption-logged
  (`N/A because ...` is a valid resolution).
- `python3 <scripts-dir>/validate_spec.py <feature>` exits 0.
- The human has approved the spec.

## Scripts

Validation scripts ship in the harness `scripts/` directory (installed as `.opencode/scripts/` in
the target project). Resolve them as `<skill-dir>/../../scripts/<name>.py`. Never run
`python3 scripts/...` from the consuming project root.