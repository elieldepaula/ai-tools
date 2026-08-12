---
name: test
description: Define a test strategy or plan and execute tests when appropriate. Use when the user asks to test, plan tests, or review test coverage. Delegates to the stack-appropriate QA subagent.
---

Test: $ARGUMENTS

Detect the stack from the codebase and delegate to the matching QA subagent:

- Magento 2 -> magento-qa
- Laravel -> laravel-qa
- Pure PHP -> php-qa
- React -> react-qa
- Vue.js -> vue-qa

## Stack detection (path-first)

1. If `$ARGUMENTS` contains a filesystem path, resolve the nearest project manifest from that path (`package.json`, `composer.json`, `app/etc/config.php`) and detect from there before scanning the repo root.
2. Prefer the most specific match from the heuristics below.
3. If multiple stacks appear (monorepo / mixed — e.g., Laravel + Vue, or a PHP backend with a JS frontend) and the path does not clearly belong to one package, ask which subsystem to test.
4. If the stack is still not obvious, ask before proceeding.

Heuristics:
- Magento 2: `composer.json` requires `magento/framework` or `magento/module-*`, or `app/code` / `app/etc/config.php` present
- Laravel: `composer.json` requires `laravel/framework`, or typical `artisan` + `app/` + `routes/` layout
- Pure PHP: PHP project without Magento or Laravel framework markers
- React: nearest `package.json` requires `react`/`react-dom` or a React metaframework (`next`, `remix`, `gatsby`), or Vite with `@vitejs/plugin-react`. Do not treat bare `.tsx`/`.jsx` alone as sufficient when another UI library is indicated.
- Vue.js: nearest `package.json` requires `vue`/`@vue/*` or `nuxt`, or `.vue` SFCs under the resolved package path

The QA agent must confirm scope, coverage targets and environments with the requester before writing a plan. It may run tests when appropriate. It never fixes code: it identifies problems and hands them back to the matching `*-developer` with reproduction steps and impact. Use coding standards only for testability/coverage gaps; escalate style, security, and architecture findings to the matching `*-reviewer`.
