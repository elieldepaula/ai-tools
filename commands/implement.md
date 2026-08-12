---
name: implement
description: Implement a feature or fix a bug. Use when the user asks to implement, code, or fix something. Delegates to the stack-appropriate developer subagent.
---

Implement: $ARGUMENTS

Detect the stack from the codebase and delegate to the matching developer subagent:

- Magento 2 -> magento-developer
- Laravel -> laravel-developer
- Pure PHP -> php-developer
- React -> react-developer
- Vue.js -> vue-developer

## Stack detection (path-first)

1. If `$ARGUMENTS` contains a filesystem path, resolve the nearest project manifest from that path (`package.json`, `composer.json`, `app/etc/config.php`) and detect from there before scanning the repo root.
2. Prefer the most specific match from the heuristics below.
3. If multiple stacks appear (monorepo / mixed — e.g., Laravel + Vue, or a PHP backend with a JS frontend) and the path does not clearly belong to one package, ask which subsystem to implement for.
4. If the stack is still not obvious, ask before proceeding.

Heuristics:
- Magento 2: `composer.json` requires `magento/framework` or `magento/module-*`, or `app/code` / `app/etc/config.php` present
- Laravel: `composer.json` requires `laravel/framework`, or typical `artisan` + `app/` + `routes/` layout
- Pure PHP: PHP project without Magento or Laravel framework markers
- React: nearest `package.json` requires `react`/`react-dom` or a React metaframework (`next`, `remix`, `gatsby`), or Vite with `@vitejs/plugin-react`. Do not treat bare `.tsx`/`.jsx` alone as sufficient when another UI library is indicated.
- Vue.js: nearest `package.json` requires `vue`/`@vue/*` or `nuxt`, or `.vue` SFCs under the resolved package path

The developer must clarify requirements when ambiguous and confirm the approach for non-trivial changes, follow existing architect decisions (escalate redesigns to the matching `*-architect`), follow the project coding standards in `.coding-standards/`, and return the implementation with relevant tests and deployment notes.
