---
description: Bootstrap the project for SDD (AGENTS.md, constitution, feature backlog)
agent: sdd
---
Run the `sdd-init` skill to bootstrap this project for the SDD workflow.

Steps:
1. Ensure `docs/scope.md` exists; if not, ask the human to create it first.
2. Create `AGENTS.md` via the `grilling` skill if it is missing (extract the `## Stack` section and
   conventions); otherwise read it and grill only on remaining ambiguity.
3. Detect the git topology with `python3 <scripts-dir>/detect_repo_topology.py`, confirm it with the
   human, and record it under `## Git` in `AGENTS.md` (`single-repo` → agent drives atomic commits;
   `multirepo` → human owns all git operations).
4. Analyze the scope with the `architect` agent and generate `specs/constitution.md` from the
   template, filling content from `AGENTS.md` and the grilling answers. Get human approval.
5. Derive `specs/features.md` (feature backlog) and have the human confirm it.
6. Report the next step: `/sdd-spec <feature>`.
