#!/usr/bin/env python3
"""
detect_repo_topology.py - deterministic git-ownership decision.

The harness lets the agent drive git only when the project is a single git
repository. When the project is a multirepo (or not a repo at all), git is
human-managed and the agent must never run git write operations. This turns
that decision into a checkable command instead of trusting the model to
remember the rule.

Definition of "single-repo": the project root is its own git work tree, i.e.
`git rev-parse --show-toplevel` succeeds and resolves to the project root.
Anything else is "multirepo": nested independent repos (e.g. backend/ and
frontend/ each with their own .git), a root that is not a repository, or no
git installed. In all of those the human owns git.

Pure standard library, zero dependencies. It shells out to `git` only.

Usage:
  python3 <scripts-dir>/detect_repo_topology.py
  python3 <scripts-dir>/detect_repo_topology.py --root /path/to/project

Exit codes: 0 detected, 1 usage error. Prints `single-repo` or `multirepo`.
"""

import argparse
import os
import shutil
import subprocess
import sys


def detect(root):
    if shutil.which("git") is None:
        return "multirepo"
    try:
        out = subprocess.run(
            ["git", "-C", root, "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.SubprocessError:
        return "multirepo"
    if out.returncode != 0:
        return "multirepo"
    toplevel = out.stdout.strip()
    if not toplevel:
        return "multirepo"
    return "single-repo" if os.path.realpath(toplevel) == os.path.realpath(root) else "multirepo"


def main(argv=None):
    p = argparse.ArgumentParser(prog="detect_repo_topology.py", description="Report whether the project is a single git repo (agent-managed git) or a multirepo (human-managed git).")
    p.add_argument("--root", default=".", help="Project root to inspect (default: current dir)")
    args = p.parse_args(argv)
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"detect_repo_topology: not a directory: {root}", file=sys.stderr)
        return 1
    print(detect(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())