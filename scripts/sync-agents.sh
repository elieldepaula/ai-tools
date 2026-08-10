#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

AGENTS_SRC="$ROOT/agents"
SKILLS_SRC="$ROOT/skills"
STANDARDS_SRC="$ROOT/coding-standards"
DIST="$ROOT/dist"
mkdir -p "$DIST"

TARGET="${1:-all}"

usage() {
  echo "Usage: $0 [all|claude|cursor|opencode]"
  echo
  echo "  all       generate .claude, .cursor and .opencode structures (default)"
  echo "  claude    generate only the .claude structure"
  echo "  cursor    generate only the .cursor structure"
  echo "  opencode  generate only the .opencode structure"
  echo
  echo "The .coding-standards folder is always generated alongside."
  exit 1
}

case "$TARGET" in
  all) TOOLS=(claude cursor opencode) ;;
  claude|cursor|opencode) TOOLS=("$TARGET") ;;
  *) usage ;;
esac

shopt -s nullglob

copy_skills() {
  local dest="$1"
  for skill in "$SKILLS_SRC"/*/; do
    [ -d "$skill" ] || continue
    cp -R "${skill%/}" "$dest/"
  done
}

detect_profile() {
  local f="$1"
  local has_tools bash_true write_false edit_false
  has_tools="$(grep -c '^tools:' "$f" || true)"
  bash_true="$(grep -c '^  bash: true' "$f" || true)"
  write_false="$(grep -c '^  write: false' "$f" || true)"
  edit_false="$(grep -c '^  edit: false' "$f" || true)"

  if [ "$has_tools" -eq 0 ]; then
    echo "full"
  elif [ "$bash_true" -ge 1 ] && [ "$write_false" -ge 1 ] && [ "$edit_false" -ge 1 ]; then
    echo "qa"
  else
    echo "readonly"
  fi
}

agent_info() {
  local f="$1"
  desc="$(sed -n 's/^description: //p' "$f" | head -1)"
  profile="$(detect_profile "$f")"
  fm_end="$(awk '/^---$/{c++; if(c==2){print NR; exit}}' "$f")"
  body="$(tail -n +$((fm_end + 1)) "$f")"
}

gen_claude() {
  local dest="$DIST/.claude"
  mkdir -p "$dest/agents" "$dest/skills"
  copy_skills "$dest/skills"
  for f in "$AGENTS_SRC"/*.md; do
    local base
    base="$(basename "$f" .md)"
    agent_info "$f"
    {
      echo "---"
      echo "name: $base"
      echo "description: $desc"
      if [ "$profile" != "full" ]; then
        case "$profile" in
          readonly) echo "tools: Read, Grep, Glob" ;;
          qa) echo "tools: Read, Grep, Glob, Bash" ;;
        esac
      fi
      echo "---"
      printf '%s\n' "$body"
    } > "$dest/agents/$base.md"
    echo "generated: $base ($profile)"
  done
}

gen_cursor() {
  local dest="$DIST/.cursor"
  mkdir -p "$dest/agents" "$dest/skills"
  copy_skills "$dest/skills"
  for f in "$AGENTS_SRC"/*.md; do
    local base
    base="$(basename "$f" .md)"
    agent_info "$f"
    {
      echo "---"
      echo "name: $base"
      echo "description: $desc"
      echo "model: inherit"
      if [ "$profile" = "readonly" ]; then
        echo "readonly: true"
      else
        echo "readonly: false"
      fi
      echo "---"
      printf '%s\n' "$body"
    } > "$dest/agents/$base.md"
    echo "generated: $base ($profile)"
  done
}

gen_opencode() {
  local dest="$DIST/.opencode"
  mkdir -p "$dest/agent" "$dest/skills"
  copy_skills "$dest/skills"
  for f in "$AGENTS_SRC"/*.md; do
    local base
    base="$(basename "$f" .md)"
    cp "$f" "$dest/agent/$base.md"
    echo "generated: $base (opencode)"
  done
}

gen_standards() {
  rm -rf "$DIST/.coding-standards"
  cp -R "$STANDARDS_SRC" "$DIST/.coding-standards"
}

for tool in "${TOOLS[@]}"; do
  rm -rf "$DIST/.$tool"
done
gen_standards

for tool in "${TOOLS[@]}"; do
  echo "[$tool]"
  "gen_$tool"
done

echo
echo "Done. Copy to the target project:"
for tool in "${TOOLS[@]}"; do
  echo "  cp -R $DIST/.$tool <project>/"
done
echo "  cp -R $DIST/.coding-standards <project>/"
