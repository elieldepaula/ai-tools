---
name: sdd-verify
description: Independent feature verification. Have the verifier subagent run a spec-anchored coverage check and a lightweight discrimination sensor, write specs/<feature>/validation.md, and confirm the completion gate (validate_state.py) passes. Runs automatically after the last task of a feature; never prompted.
---

## What I do

Close out a feature with an independent quality gate. The Verifier (author != verifier) re-derives
coverage from the spec, tests that the tests can detect regressions (discrimination sensor), writes
a persisted report, and the deterministic gate confirms the report is real.

## Steps

1. Load `sdd-context` for the feature. Note the repo topology (`single-repo` vs `multirepo`).
   Confirm all tasks are implemented and gate-verified; in a `single-repo` they must also be
   committed.
2. Dispatch a fresh `verifier` subagent (read-only) with:
   - `specs/<feature>/spec.md` (ACs = source of truth)
   - the git diff surface for the feature: the commit range in a `single-repo`; in a `multirepo`,
     the per-repo diff (read-only `git diff`/`git log` in each repo, or the commit hashes the
     human provides) — the agent never commits, branches, or creates worktrees there
   - the test files in scope
   - this skill as its operating checklist.
3. The Verifier returns a compact verdict (PASS/FAIL) and a ranked gap list.
4. On FAIL: route the ranked gaps back to an implementer as fix tasks, re-verify. Bound to **3
   fix→re-verify iterations** before escalating to the user.
5. On PASS: run the deterministic completion gate
   `python3 <scripts-dir>/validate_state.py <feature>`. Non-zero exit = the feature is NOT done.
6. Distill lessons: for each grounded failure (surviving mutant, spec-precision gap, failed AC,
   SPEC_DEVIATION) run `python3 <scripts-dir>/lessons.py add --feature <feature> --signal <signal>
   --source <file:line> --text "<terse lesson>"`. A clean PASS records nothing.

## Verifier operating checklist

### Spec-anchored acceptance criteria

For each acceptance criterion, build this table:

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --------- | -------------------- | ----------------------- | ------ |
| WHEN X THEN Y | precise value/state from spec | `path/to/test.php:42` - `expect(...)` | PASS / GAP / spec-precision gap |

- Evidence-or-zero: no `file:line` citation = NOT covered. Show the search before concluding missing.
- Asserted values must match spec-defined outcomes; where the spec is imprecise, mark the gap.

### Discrimination sensor (lightweight)

1. Capture baseline: `git status --porcelain` (read-only; per repo in a `multirepo`).
2. Create scratch from **temp file copies** only — copy the affected files to a temp dir and run
   the tests there. Never `git worktree add` (a git write command — forbidden in a `multirepo` and
   unnecessary everywhere) and never `git stash`.
3. Inject 1-3 behavior-level faults in the scratch (proportional to risk):
   - flip a boolean condition (`>` → `>=`, `if (x)` → `if (!x)`)
   - change a return value (wrong status code, wrong field, zero instead of computed)
   - off-by-one (loop bound, slice index)
   - remove a required side effect
4. Run the focused tests in the scratch. Confirm the mutant is **killed** (tests FAIL).
5. Discard the scratch. Verify real-tree `git status --porcelain` matches baseline.
6. Surviving mutant → fix task to strengthen the assertion.

**Forbidden:** `git worktree`, `git stash` / `git stash pop` — they write git state and can leave
faults in the real tree.

### Validation report template

Write `specs/<feature>/validation.md`:

```markdown
# <Feature> Validation

**Date**: YYYY-MM-DD
**Spec**: specs/<feature>/spec.md
**Diff surface**: <commit range (single-repo) or per-repo diff / human-provided commit hashes (multirepo)>
**Verifier**: independent sub-agent (author != verifier)

## Validation: [PASS | FAIL]

(Write the verdict inline on the heading line — `## Validation: PASS` or
`## Validation: FAIL`. A verdict on a separate line is not detected by the
completion gate.)

## Spec-Anchored Acceptance Criteria
| Criterion | Spec-defined outcome | file:line + assertion | Result |

## Discrimination Sensor
| Mutation | File:line | Description | Killed? |

## Gate Check
- Command / Result / Test count before / after / delta

## Requirement Traceability
| Requirement | Previous | New |

## Summary
**Overall**: Ready / Issues / Not Ready
**Ranked gaps**: ...
```

## Definition of done

- `specs/<feature>/validation.md` exists, verdict filled to PASS, and cites at least one
  `file:line` evidence.
- `python3 <scripts-dir>/validate_state.py <feature>` exits 0.
- Lessons distilled for every grounded failure (or none occurred).

## Scripts

Validation scripts ship in the harness `scripts/` directory (installed as
`.opencode/scripts/` in the target project). Resolve them as
`<skill-dir>/../../scripts/<name>.py` (from `skills/sdd-verify/` that is `.opencode/scripts/`), or
pass the absolute path if the harness is installed elsewhere. Never run `python3 scripts/...` from
the consuming project root.