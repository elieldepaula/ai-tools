---
name: implement
description: Implement a feature or fix a bug. Use when the user asks to implement, code, or fix something. Delegates to the stack-appropriate developer subagent.
---

Implement: $ARGUMENTS

Detect the stack from the codebase and delegate to the matching developer subagent:

- Magento 2 -> magento-developer
- Laravel -> laravel-developer
- Pure PHP -> php-developer

Stack detection heuristics (prefer the most specific match):
- Magento 2: `composer.json` requires `magento/framework` or `magento/module-*`, or `app/code` / `app/etc/config.php` present
- Laravel: `composer.json` requires `laravel/framework`, or typical `artisan` + `app/` + `routes/` layout
- Pure PHP: PHP project without Magento or Laravel framework markers

If Magento and Laravel both appear (monorepo / mixed), or the path in `$ARGUMENTS` spans multiple stacks, ask which subsystem to implement for — or detect from the path when it clearly belongs to one package. If the stack is not obvious, ask before proceeding.

The developer must clarify requirements when ambiguous and confirm the approach for non-trivial changes, follow existing architect decisions (escalate redesigns to the matching `*-architect`), follow the project coding standards in `.coding-standards/`, and return the implementation with relevant tests and deployment notes.
