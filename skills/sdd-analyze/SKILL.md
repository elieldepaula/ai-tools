---
name: sdd-analyze
description: Read-only consistency and quality analysis across spec.md, design.md, and tasks.md — including requirement traceability and coding-standard coverage. Have the reviewer report conflicts, gaps, and ambiguities; fix at the source, never by editing the artifacts directly. Run before implementation, and optionally after.
---

## What I do

Cross-check the artifacts of a feature and report conflicts, gaps, and ambiguities — for example a
task with no matching requirement, a plan choice that contradicts the spec, an acceptance criterion
with no covering task, or a requirement ID with no trace. Read-only: this phase never edits
artifacts.

## Steps

1. Load `sdd-context` for the feature. Require `spec.md` (and `design.md`/`tasks.md` if present).
2. Delegate the analysis to the `reviewer` subagent (read-only). Ask for a severity-graded report:
   - Requirements without a plan item or task.
   - Plan decisions contradicting the spec or constitution.
   - Tasks with no matching requirement (orphans).
   - Ambiguous acceptance criteria (not EARS-shaped / no precise outcome).
   - **Traceability gaps**: requirement IDs in the traceability table with no covering task, or
     tasks with no requirement ID.
   - **Standards check**: do plan/task references to `.coding-standards/` docs exist, and do they
     cover the stacks being implemented? If a referenced doc is missing, flag it.
3. Present the report to the human with recommended remediations.
4. Loop back to the phase that owns each issue — `sdd-spec`/`sdd-checklist` for requirement problems,
   `sdd-plan` for design problems, `sdd-tasks` to regenerate the task list — then re-run `sdd-analyze`
   until clean.

## Definition of done

The report is clean (no conflicts, gaps, or ambiguities) or every finding has been remediated at its
source. You never patch the artifacts directly to silence a finding.