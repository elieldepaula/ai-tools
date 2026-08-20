---
description: Build the harness bundle and install it into a project
agent: sdd
---
Run the `install.sh` script from the harness repository root:

```
!`bash install.sh 2>&1 || true`
```

If it produced `dist/.opencode/`, explain the next step: copy that folder into the target project as
its `.opencode/` directory, and copy `dist/.coding-standards/` into the target project as its
`.coding-standards/` directory. Then remind the human to create `docs/` with `docs/scope.md` in the
target project and run `/sdd-init`.