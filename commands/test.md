---
name: test
description: Define a test strategy or plan and execute tests when appropriate. Use when the user asks to test, plan tests, or review test coverage. Delegates to the stack-appropriate QA subagent.
---

Test: $ARGUMENTS

Detect the stack from the codebase and delegate to the matching QA subagent:

- Magento 2 -> magento-qa
- Laravel -> laravel-qa
- Pure PHP -> php-qa

Stack detection heuristics (prefer the most specific match):
- Magento 2: `composer.json` requires `magento/framework` or `magento/module-*`, or `app/code` / `app/etc/config.php` present
- Laravel: `composer.json` requires `laravel/framework`, or typical `artisan` + `app/` + `routes/` layout
- Pure PHP: PHP project without Magento or Laravel framework markers

If Magento and Laravel both appear (monorepo / mixed), or the path in `$ARGUMENTS` spans multiple stacks, ask which subsystem to test — or detect from the path when it clearly belongs to one package. If the stack is not obvious, ask before proceeding.

The QA agent must confirm scope, coverage targets and environments with the requester before writing a plan. It may run tests when appropriate. It never fixes code: it identifies problems and hands them back to the matching `*-developer` with reproduction steps and impact. Use coding standards only for testability/coverage gaps; escalate style, security, and architecture findings to the matching `*-reviewer`.
