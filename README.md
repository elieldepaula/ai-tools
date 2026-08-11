# AI Tools

A collection of reusable AI coding agents, portable skills, and coding standards for development workflows. Supports **opencode**, **Claude Code**, and **Cursor** through a single sync script.

- 12 specialized agents (architect, developer, QA, reviewer) for **Magento 2**, **vanilla PHP**, and **Laravel**
- 4 portable skills (Agent Skills / `SKILL.md` format): `caveman`, `grilling`, `grill-me`, `planning-with-files`
- 4 slash commands (`/design`, `/implement`, `/test`, `/review`) distributed as skills across all tools
- 12 reusable coding standards in `coding-standards/`
- One script generates the correct agent/skill/command layout for each tool

## Installation

```bash
git clone https://github.com/elieldepaula/ai-tools.git
cd ai-tools
```

## Usage

Generate agents and skills for one or more tools:

```bash
scripts/sync-agents.sh            # all tools (opencode, Claude Code, Cursor)
scripts/sync-agents.sh opencode   # only opencode
scripts/sync-agents.sh claude     # only Claude Code
scripts/sync-agents.sh cursor     # only Cursor
```

The script writes everything to `dist/`:

```
dist/
├── .claude/
│   ├── agents/        # Claude Code agents (tools: Read, Grep, Glob[, Bash])
│   └── skills/        # skills + commands (/design, /implement, ...)
├── .cursor/
│   ├── agents/        # Cursor agents (readonly: true|false)
│   └── skills/
├── .opencode/
│   ├── agent/         # opencode agents (canonical format)
│   └── skills/
└── .coding-standards/
```

Agent profiles are translated per tool:

| Profile  | opencode / canonical                          | Claude Code                                   | Cursor         |
| -------- | --------------------------------------------- | --------------------------------------------- | -------------- |
| Read-only | `tools: {bash: false, write: false, edit: false}` | `tools: Read, Grep, Glob`                    | `readonly: true` |
| QA       | `tools: {bash: true, write: false, edit: false}`  | `tools: Read, Grep, Glob, Bash`              | `readonly: false` |
| Full     | (no `tools` block)                            | (no `tools` field)                           | `readonly: false` |

Cursor cannot express “bash without write,” so QA agents map to `readonly: false`. The agent body still requires never fixing or editing application code; follow that instruction even when write tools are available.

Then copy the generated folder(s) into your target project:

```bash
cp -R dist/.opencode/. <your-project>/
cp -R dist/.claude/.   <your-project>/
cp -R dist/.cursor/.   <your-project>/
```

## Agents

### Roles

| Role | Profile | Responsibility |
| ---- | ------- | ------------- |
| Architect | Read-only | Designs solutions, module/package/application structure, and technical decisions |
| Developer | Full | Implements features, fixes bugs, and refactors code |
| QA | Bash only | Defines test strategies and plans, runs/analyzes tests, reviews coverage — identifies problems and hands them back to the developer, never fixes code; general standards/security review belongs to the Reviewer |
| Reviewer | Read-only | Reviews code for security, performance, patterns, and standards |

### Available agents

#### Magento 2

| Agent | Profile | Description |
| ----- | ------- | ----------- |
| `magento-architect` | read-only | Systems architect for Magento 2: scalable solutions, module structure, design patterns, technical decisions |
| `magento-developer` | full | Implements features, fixes bugs, and writes code following Magento ecosystem standards |
| `magento-qa` | qa | Test strategies, plans, running/analyzing tests, and coverage reviews for Magento 2 |
| `magento-reviewer` | readonly | Reviews code for Magento 2 practices, security, performance, and PSR standards |

#### Vanilla PHP

| Agent | Profile | Description |
| ----- | ------- | ----------- |
| `php-architect` | read-only | Systems architect for pure PHP: package structure, design patterns, technical decisions |
| `php-developer` | full | Implements features and fixes bugs following PHP community standards (PSR) |
| `php-qa` | qa | Test strategies, plans, running/analyzing tests, and coverage reviews for pure PHP |
| `php-reviewer` | readonly | Reviews code for PHP practices, security, performance, and PSR standards |

#### Laravel

| Agent | Profile | Description |
| ----- | ------- | ----------- |
| `laravel-architect` | read-only | Systems architect for Laravel: application structure, design patterns, technical decisions |
| `laravel-developer` | full | Implements features and fixes bugs following Laravel ecosystem standards |
| `laravel-qa` | qa | Test strategies, plans, running/analyzing tests, and coverage reviews for Laravel |
| `laravel-reviewer` | readonly | Reviews code for Laravel practices, security, performance, and PSR standards |

### Using the agents

Agents run as subagents in each tool:

| Tool | How to invoke | Example |
| ---- | ------------- | ------- |
| opencode | `@` mention in the message | `@magento-reviewer review the changes in @src/app/code/Foo` |
| Claude Code | mention the agent by name; Claude delegates via the Agent tool | `Use the laravel-reviewer subagent to review the auth module.` |
| Cursor | `@` mention in Agent chat | `@php-qa write a test plan for the new checkout flow` |

Example review pipeline:

```
@php-architect design the module structure for the reporting feature
@php-developer implement the architect's plan
@php-qa build a test plan and run the test suite
@php-reviewer review the pull request against the coding standards
```

## Skills

| Skill | What it does | When to use |
| ----- | ------------- | ----------- |
| `caveman` | Ultra-compressed communication mode; cuts token usage ~75% while keeping full technical accuracy | "be brief", token efficiency, dense summaries |
| `grilling` | Relentless interview of a plan/decision using a design tree explored in rounds | Stress-testing a plan, decision, or idea |
| `grill-me` | Shortcut that activates the `grilling` interview | Only when you explicitly ask to be grilled |
| `planning-with-files` | Manus-style file-based planning (`task_plan.md`, `findings.md`, `progress.md`) with session recovery | Complex multi-step tasks (5+ tool calls) |

### Using the skills

Skills are loaded automatically by the agent when relevant, or can be invoked manually:

| Tool | Invocation | Example |
| ---- | ---------- | ------- |
| opencode | `/` command (or `$skill` inline in newer versions) | `/caveman summarize the findings` |
| Claude Code | `/` command | `/planning-with-files plan the migration` |
| Cursor | `/` command in Agent chat | `/grilling grill my design` |

## Commands

Commands are task shortcuts distributed as skills, so they work the same way in every tool (`/command`). Each one detects the codebase stack and delegates to the matching subagent:

| Command | Delegates to | Example |
| ------- | ------------ | ------- |
| `/design` | `*-architect` | `/design the order checkout module` |
| `/implement` | `*-developer` | `/implement the password reset flow` |
| `/test` | `*-qa` | `/test the payment integration` |
| `/review` | `*-reviewer` | `/review the changes in @src/app` |

Author new commands as `commands/<name>.md` with `name` and `description` frontmatter; the sync script turns each one into a `skills/<name>/SKILL.md` for every tool.

## Project structure

```
ai-tools/
├── agents/               # canonical agents (source of truth)
├── skills/               # portable skills (SKILL.md format)
├── commands/             # slash commands, distributed as skills
├── coding-standards/       # coding standards referenced by agents (as .coding-standards in dist/)
├── scripts/
│   └── sync-agents.sh    # multi-tool generation script
└── dist/                 # generated output per tool
```

## Credits

The following skills are derived from original works by their respective authors:

| Skill               | Author                          | Source                                                  |
| ------------------- | ------------------------------- | ------------------------------------------------------- |
| `caveman`           | Julius Brussee                  | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) |
| `grilling`          | Matt Pocock                     | [mattpocock/skills](https://github.com/mattpocock/skills)        |
| `grill-me`          | Matt Pocock                     | [mattpocock/skills](https://github.com/mattpocock/skills)        |
| `planning-with-files` | Ahmad Othman Ammar Adi         | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) |

The agents and coding standards in this repository are original to this project.

## License

[MIT](LICENSE)
