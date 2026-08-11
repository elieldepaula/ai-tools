---
name: implement
description: Implement a feature or fix a bug. Use when the user asks to implement, code, or fix something. Delegates to the stack-appropriate developer subagent.
---

Implement: $ARGUMENTS

Detect the stack from the codebase (Magento 2, Laravel, or pure PHP) and delegate to the matching developer subagent:

- Magento 2 -> magento-developer
- Laravel -> laravel-developer
- Pure PHP -> php-developer

If the stack is not obvious, ask before proceeding. The developer must clarify requirements when ambiguous and confirm the approach for non-trivial changes, follow the project coding standards in `.coding-standards/`, and return the implementation with relevant tests and deployment notes.
