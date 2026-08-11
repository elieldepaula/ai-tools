---
name: test
description: Define and run a test strategy or plan. Use when the user asks to test, plan tests, or review test coverage. Delegates to the stack-appropriate QA subagent.
---

Test plan for: $ARGUMENTS

Detect the stack from the codebase (Magento 2, Laravel, or pure PHP) and delegate to the matching QA subagent:

- Magento 2 -> magento-qa
- Laravel -> laravel-qa
- Pure PHP -> php-qa

The QA agent must confirm scope, coverage targets and environments with the requester before writing a plan. It never fixes code: it identifies problems and hands them back to the developer with reproduction steps and impact. Verify code under test against the project coding standards in `.coding-standards/`.
