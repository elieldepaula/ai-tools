---
name: design
description: Design an architectural solution. Use when the user asks to design, plan architecture, or propose a solution structure. Delegates to the stack-appropriate architect subagent.
---

Design an architectural solution for: $ARGUMENTS

Detect the stack from the codebase (Magento 2, Laravel, or pure PHP) and delegate to the matching architect subagent:

- Magento 2 -> magento-architect
- Laravel -> laravel-architect
- Pure PHP -> php-architect

If the stack is not obvious, ask before proceeding. The architect must confirm constraints (stack version, project boundaries, existing architecture, deployment environment) before proposing, design against the project coding standards in `.coding-standards/`, and return context, proposed solution, rationale, alternatives considered, and a diagram/file structure when applicable.
