---
name: design
description: Design an architectural solution. Use when the user asks to design, plan architecture, or propose a solution structure. Delegates to the stack-appropriate architect subagent.
---

Design: $ARGUMENTS

Detect the stack from the codebase and delegate to the matching architect subagent:

- Magento 2 -> magento-architect
- Laravel -> laravel-architect
- Pure PHP -> php-architect

Stack detection heuristics (prefer the most specific match):
- Magento 2: `composer.json` requires `magento/framework` or `magento/module-*`, or `app/code` / `app/etc/config.php` present
- Laravel: `composer.json` requires `laravel/framework`, or typical `artisan` + `app/` + `routes/` layout
- Pure PHP: PHP project without Magento or Laravel framework markers

If Magento and Laravel both appear (monorepo / mixed), or the path in `$ARGUMENTS` spans multiple stacks, ask which subsystem to design for — or detect from the path when it clearly belongs to one package. If the stack is not obvious, ask before proceeding.

The architect must confirm constraints (stack version, project boundaries, existing architecture, deployment environment) before proposing, design against the project coding standards in `.coding-standards/`, and return context, proposed solution, rationale, alternatives considered, and a diagram/file structure when applicable.
