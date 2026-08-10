# AI Tools

A collection of reusable AI coding agents, portable skills, and coding standards for development workflows. Supports **opencode**, **Claude Code**, and **Cursor** through a single sync script.

- 12 specialized agents (architect, developer, QA, reviewer) for **Magento 2**, **vanilla PHP**, and **Laravel**
- 4 portable skills (Agent Skills / `SKILL.md` format): `caveman`, `grilling`, `grill-me`, `planning-with-files`
- 12 reusable coding standards in `coding-standards/`
- One script generates the correct agent/skill layout for each tool

## Installation

```bash
git clone https://github.com/<your-username>/ai-tools.git
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
│   └── skills/
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

Then copy the generated folder(s) into your target project:

```bash
cp -R dist/.opencode/. <your-project>/
cp -R dist/.claude/.   <your-project>/
cp -R dist/.cursor/.   <your-project>/
```

## Project structure

```
ai-tools/
├── agents/               # canonical agents (source of truth)
├── skills/               # portable skills (SKILL.md format)
├── coding-standards/    # coding standards referenced by agents (as .coding-standards in dist/)
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
