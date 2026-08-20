#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$ROOT_DIR/dist"
BUNDLE_DIR="$DIST_DIR/.opencode"

echo "Building harness bundle into $BUNDLE_DIR ..."
echo

mkdir -p "$DIST_DIR"
rm -rf "$BUNDLE_DIR"
mkdir -p "$BUNDLE_DIR"

for dir in agents skills commands scripts; do
  if [ -d "$ROOT_DIR/$dir" ]; then
    cp -R "$ROOT_DIR/$dir" "$BUNDLE_DIR/"
    rm -rf "$BUNDLE_DIR/$dir/__pycache__" 2>/dev/null || true
    echo "  copied $dir/"
  else
    echo "  WARN: $dir/ not found, skipping"
  fi
done

if [ -d "$ROOT_DIR/coding-standards" ]; then
  rm -rf "$DIST_DIR/.coding-standards"
  cp -R "$ROOT_DIR/coding-standards" "$DIST_DIR/.coding-standards"
  echo "  copied coding-standards/ -> .coding-standards/"
else
  echo "  WARN: coding-standards/ not found, skipping"
fi

echo
echo "Done. Install into your target project:"
echo "  cp -R \"$BUNDLE_DIR\" /path/to/your/project/.opencode"
echo "  cp -R \"$DIST_DIR/.coding-standards\" /path/to/your/project/.coding-standards"
