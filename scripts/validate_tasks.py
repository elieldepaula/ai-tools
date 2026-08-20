#!/usr/bin/env python3
"""
validate_tasks.py - deterministic pre-approval checks for a feature's tasks.

Turns the pre-approval checks (task granularity, dependency coherence, test
co-location) into a checkable pass/fail run BEFORE tasks are presented for
approval, instead of trusting the model to build the tables by hand. Pure
standard library, zero dependencies. Operates only on the markdown artifacts
(`specs/<feature>/tasks.md` index + `specs/<feature>/tasks/<id>-<slug>.md`
detail files), so it is stack-agnostic and tool-agnostic.

What it checks (heuristic markdown inspection, not a full parser):
  ERROR  - a required section is missing from tasks.md
  ERROR  - a task detail file is missing `## Tests` or `## Gate`
  ERROR  - a task depends on a task id that does not exist
  ERROR  - a dependency on the task itself (self-loop)
  WARN   - a task's `Files likely touched` names multiple files (granularity smell)
  WARN   - a task says `Tests: none` (confirm the coverage matrix agrees)
  WARN   - a task detail file has no matching index entry (and vice-versa)

Usage:
  python3 <scripts-dir>/validate_tasks.py [target] [--root DIR] [--strict]

  target    Path to a tasks.md, a feature directory, or a project root.
            Omitted -> auto-detect the single feature under <root>/specs/.
  --root    Project root that contains specs/ (default: current dir).
  --strict  Treat warnings as errors.

Exit codes: 0 pass, 1 errors found (or warnings under --strict), 2 usage error.
"""

import argparse
import os
import re
import sys

REQUIRED_SECTIONS = ["Test Coverage Matrix", "Gate Check Commands", "Execution Plan", "Task Breakdown"]
INDEX_RE = re.compile(r"^\s*-\s*\[\s*x?\s*\]\s+(T\d+)\b", re.IGNORECASE)
TASK_ID_RE = re.compile(r"^(T\d+)\b", re.IGNORECASE)
FIELD_RE = {
    "depends": re.compile(r"^#{1,4}\s+Depends on\s*$", re.IGNORECASE),
    "tests": re.compile(r"^#{1,4}\s+Tests\s*$", re.IGNORECASE),
    "gate": re.compile(r"^#{1,4}\s+Gate\s*$", re.IGNORECASE),
    "files": re.compile(r"^#{1,4}\s+Files likely touched\s*$", re.IGNORECASE),
}
FILE_HINT_RE = re.compile(r"[\w./-]+\.\w{1,6}\b")


def resolve_tasks_dir(target, root):
    """Return the feature dir (containing tasks.md) from a file, dir, or auto-detect."""
    if target:
        if os.path.isfile(target):
            return os.path.dirname(target)
        if os.path.isdir(target):
            if os.path.isfile(os.path.join(target, "tasks.md")):
                return target
            return _autodetect(target)
        cand = os.path.join(root, "specs", target)
        if os.path.isfile(os.path.join(cand, "tasks.md")):
            return cand
        return None
    return _autodetect(root)


def _autodetect(root):
    base = os.path.join(root, "specs")
    if not os.path.isdir(base):
        return None
    features = [d for d in sorted(os.listdir(base)) if os.path.isfile(os.path.join(base, d, "tasks.md"))]
    if len(features) == 1:
        return os.path.join(base, features[0])
    if len(features) == 0:
        return None
    raise SystemExit(
        "validate_tasks: multiple features found; pass one explicitly:\n  "
        + "\n  ".join(os.path.join(base, f) for f in features)
    )


def section_present(lines, name):
    return any(re.match(r"^#{1,4}\s+" + re.escape(name) + r"\b", ln.strip()) for ln in lines)


def read_index(tasks_md):
    """Return set of task ids from the `- [ ] T01 - ...` index lines."""
    ids = set()
    if not os.path.isfile(tasks_md):
        return ids
    with open(tasks_md, "r", encoding="utf-8") as f:
        for ln in f:
            m = INDEX_RE.match(ln)
            if m:
                ids.add(m.group(1).upper())
    return ids


def read_detail(path):
    """Return (tests, gate, deps, files) for a task detail file."""
    tests = gate = files = None
    deps = set()
    current = None
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    for ln in lines:
        stripped = ln.strip()
        for key, pat in FIELD_RE.items():
            if pat.match(stripped):
                current = key
                break
        else:
            if current is None:
                continue
        if current == "tests":
            if "Tests" in stripped or stripped == "" or re.match(r"^#{1,4}\s", stripped):
                continue
            tests = stripped.lstrip("-* ").strip() or None
            current = None
        elif current == "gate":
            if "Gate" in stripped or stripped == "" or re.match(r"^#{1,4}\s", stripped):
                continue
            gate = stripped.lstrip("-* ").strip() or None
            current = None
        elif current == "depends":
            if "Depends on" in stripped or re.match(r"^#{1,4}\s", stripped):
                current = None
                continue
            if re.search(r"\bT\d+\b", stripped, re.IGNORECASE):
                for e in re.findall(r"\bT\d+\b", stripped, re.IGNORECASE):
                    deps.add(e.upper())
        elif current == "files":
            if "Files likely touched" in stripped or re.match(r"^#{1,4}\s", stripped):
                current = None
                continue
            if stripped:
                files = (files or "") + " " + stripped
    return tests, gate, deps, files


def check(feature_dir):
    tasks_md = os.path.join(feature_dir, "tasks.md")
    tasks_sub = os.path.join(feature_dir, "tasks")
    errors, warnings = [], []

    if not os.path.isfile(tasks_md):
        errors.append(f"missing tasks.md in {feature_dir}")
        return errors, warnings

    with open(tasks_md, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    for name in REQUIRED_SECTIONS:
        if not section_present(lines, name):
            errors.append(f"missing required section in tasks.md: ## {name}")

    index_ids = read_index(tasks_md)
    if not index_ids:
        errors.append("no task index lines (`- [ ] T01 - <slug>`) found in tasks.md")

    detail_files = []
    if os.path.isdir(tasks_sub):
        detail_files = sorted(os.listdir(tasks_sub))
    detail_ids = set()
    for fn in detail_files:
        m = TASK_ID_RE.match(fn)
        if m:
            detail_ids.add(m.group(1).upper())
    if detail_files and not detail_ids:
        warnings.append("tasks/ directory exists but no files match `Tnn-<slug>.md`")

    for fn in detail_files:
        m = TASK_ID_RE.match(fn)
        if not m:
            warnings.append(f"unrecognized task file in tasks/: {fn}")
            continue
        tid = m.group(1).upper()
        tests, gate, deps, files = read_detail(os.path.join(tasks_sub, fn))
        if tests is None:
            errors.append(f"{tid}: missing `## Tests` field")
        elif tests.lower().startswith("none"):
            warnings.append(f"{tid}: Tests: none - confirm the Test Coverage Matrix says 'none' for this layer")
        if gate is None:
            errors.append(f"{tid}: missing `## Gate` field")
        if files:
            hit = FILE_HINT_RE.findall(files)
            if len(set(hit)) > 1:
                warnings.append(f"{tid}: `Files likely touched` names multiple files {sorted(set(hit))} - granularity smell, consider splitting")
        for dep in deps:
            if dep == tid:
                errors.append(f"{tid}: depends on itself (self-loop)")
            elif dep not in index_ids and dep not in detail_ids:
                errors.append(f"{tid}: depends on {dep}, which has no task file and no index entry")

    # Index/detail parity.
    for tid in sorted(index_ids - detail_ids):
        if not any(fn.startswith(tid + "-") for fn in detail_files):
            warnings.append(f"index lists {tid} but no detail file under tasks/ matches {tid}-*")
    for tid in sorted(detail_ids - index_ids):
        warnings.append(f"detail file exists for {tid} but no `- [ ] {tid}` index line in tasks.md")

    return errors, warnings


def main(argv=None):
    p = argparse.ArgumentParser(prog="validate_tasks.py", description="Pre-approval checks for a feature's tasks.")
    p.add_argument("target", nargs="?", default=None)
    p.add_argument("--root", default=".")
    p.add_argument("--strict", action="store_true")
    args = p.parse_args(argv)

    feature_dir = resolve_tasks_dir(args.target, args.root)
    if not feature_dir:
        print("validate_tasks: could not locate a tasks.md. Pass a path or run from the project root.", file=sys.stderr)
        return 2

    errors, warnings = check(feature_dir)
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    fail = errors or (warnings and args.strict)
    print(f"\nvalidate_tasks: {len(errors)} error(s), {len(warnings)} warning(s) for {feature_dir}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())