---
name: design
description: Design an architectural solution. Use when the user asks to design, plan architecture, or propose a solution structure. Delegates to the stack-appropriate architect subagent.
---

Design: $ARGUMENTS

Detect the stack from the codebase and delegate to the matching architect subagent:

- Magento 2 -> magento-architect
- Laravel -> laravel-architect
- Pure PHP -> php-architect
- React -> react-architect
- Vue.js -> vue-architect

## Stack detection (path-first)

1. If `$ARGUMENTS` contains a filesystem path, resolve the nearest project manifest from that path (`package.json`, `composer.json`, `app/etc/config.php`) and detect from there before scanning the repo root.
2. Prefer the most specific match from the heuristics below.
3. If multiple stacks appear (monorepo / mixed — e.g., Laravel + Vue, or a PHP backend with a JS frontend) and the path does not clearly belong to one package, ask which subsystem to design for.
4. If the stack is still not obvious, ask before proceeding.

Heuristics:
- Magento 2: `composer.json` requires `magento/framework` or `magento/module-*`, or `app/code` / `app/etc/config.php` present
- Laravel: `composer.json` requires `laravel/framework`, or typical `artisan` + `app/` + `routes/` layout
- Pure PHP: PHP project without Magento or Laravel framework markers
- React: nearest `package.json` requires `react`/`react-dom` or a React metaframework (`next`, `remix`, `gatsby`), or Vite with `@vitejs/plugin-react`. Do not treat bare `.tsx`/`.jsx` alone as sufficient when another UI library is indicated.
- Vue.js: nearest `package.json` requires `vue`/`@vue/*` or `nuxt`, or `.vue` SFCs under the resolved package path

The architect must confirm constraints (stack version, project boundaries, existing architecture, deployment environment) before proposing, design against the project coding standards in `.coding-standards/`, and return context, proposed solution, rationale, alternatives considered, and a diagram/file structure when applicable.
