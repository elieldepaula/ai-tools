---
name: review
description: Review code for correctness, security, performance and standards. Use when the user asks to review code, a diff, or a pull request. Delegates to the stack-appropriate reviewer subagent.
---

Review: $ARGUMENTS

Detect the stack from the codebase and delegate to the matching reviewer subagent:

- Magento 2 -> magento-reviewer
- Laravel -> laravel-reviewer
- Pure PHP -> php-reviewer

Stack detection heuristics (prefer the most specific match):
- Magento 2: `composer.json` requires `magento/framework` or `magento/module-*`, or `app/code` / `app/etc/config.php` present
- Laravel: `composer.json` requires `laravel/framework`, or typical `artisan` + `app/` + `routes/` layout
- Pure PHP: PHP project without Magento or Laravel framework markers

If Magento and Laravel both appear (monorepo / mixed), or the path in `$ARGUMENTS` spans multiple stacks, ask which subsystem to review — or detect from the path when it clearly belongs to one package. If the stack is not obvious, ask before proceeding.

The reviewer never modifies files. It must check the code against the project coding standards in `.coding-standards/`, prioritize security and performance issues, report each issue with severity, location, description and suggestion, and hand actionable findings to the matching `*-developer`. Test strategy and coverage planning belong to the matching `*-qa`.
