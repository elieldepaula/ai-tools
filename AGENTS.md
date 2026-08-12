# AGENTS.md

This is a **meta-repo**, not application code. It is the source of truth for a reusable AI-agent stack (agents, skills, slash commands, coding standards) that gets generated into opencode / Claude Code / Cursor layouts.

## Language & planning

- Always communicate in English (agent bodies, descriptions, docs).
- Always use the `grilling` skill for planning work before proposing or implementing anything non-trivial.

## The one command that matters

```bash
scripts/sync-agents.sh          # generate all tools
scripts/sync-agents.sh opencode # claude | cursor | opencode, plus .coding-standards always
```

- Source of truth is `agents/`, `skills/`, `commands/`, `coding-standards/`.
- `dist/` is **generated and gitignored**. Never hand-edit `dist/`; edit sources and re-run the script, then spot-check the generated frontmatter.

## Source layout

- `agents/*.md` — 20 canonical agents (`<stack>-<role>`: magento/php/laravel/react/vue × architect/developer/qa/reviewer). Already in opencode format; opencode copies them as-is, claude/cursor regenerate the frontmatter.
- `skills/<name>/SKILL.md` — each skill is a folder, copied wholesale into every tool.
- `commands/<name>.md` — slash commands, converted to `skills/<name>/SKILL.md` per tool.
- `coding-standards/*.md` — copied to `dist/.coding-standards/`. Agents link to them as `.coding-standards/<file>.md`, so that folder must live at the target project's root.

## Agent profile system (critical gotcha)

The generator infers each agent's tool profile by regex over the `tools:` frontmatter (`detect_profile()` in `scripts/sync-agents.sh`), then translates it per tool:

| Profile | Frontmatter (exact, 2-space indent) | opencode | Claude | Cursor |
|---|---|---|---|---|
| full | (no `tools:` block) | no `tools` | no field | `readonly: false` |
| qa | `tools:` + `bash: true` + `write: false` + `edit: false` | as-is | + Bash | `readonly: false` |
| readonly | `tools:` + `bash: false` + `write: false` + `edit: false` | as-is | Read, Grep, Glob | `readonly: true` |

- Deviating from these exact blocks (e.g. 4-space indent, extra keys) silently changes the generated profile.
- Cursor cannot express "bash without write": QA agents map to `readonly: false`, so their body must still explicitly forbid fixing/editing code.
- Roles: architect = readonly, developer = full, qa = run tests only (never fix), reviewer = readonly.

## Frontmatter conventions

- `description:` and `name:` are parsed with `sed -n 's/^description: //p'` / `s/^name: //p` in the generator. They must be **single-line** values. Folded `description: >` multi-line styles (as used in `skills/caveman/SKILL.md`) are fine only for skills (copied wholesale), not for agents or commands.
- Agents: `description`, `mode: subagent`, optional `tools:` (see above).
- Commands: `name:` must equal the filename or the script warns; `description:` required.
- Agent bodies reference internal skills by name (`planning-with-files`, `grilling`, `caveman`) and assume they ship with the generated stack.

## Workflow

1. Edit sources in `agents/`, `skills/`, `commands/`, or `coding-standards/`.
2. Run `scripts/sync-agents.sh` (use `git status` to confirm `dist/` was not committed — it is gitignored).
3. Adding a new agent means adding one of the exact profile blocks above plus a single-line description.
