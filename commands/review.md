---
name: review
description: Review code for correctness, security, performance and standards. Use when the user asks to review code, a diff, or a pull request. Delegates to the stack-appropriate reviewer subagent.
---

Review: $ARGUMENTS

Detect the stack from the codebase (Magento 2, Laravel, or pure PHP) and delegate to the matching reviewer subagent:

- Magento 2 -> magento-reviewer
- Laravel -> laravel-reviewer
- Pure PHP -> php-reviewer

The reviewer never modifies files. It must check the code against the project coding standards in `.coding-standards/`, prioritize security and performance issues, and report each issue with severity, location, description and suggestion.
