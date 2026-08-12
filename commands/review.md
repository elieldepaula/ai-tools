---
name: review
description: Review code for correctness, security, performance and standards. Use when the user asks to review code, a diff, or a pull request. Delegates to the stack-appropriate reviewer subagent.
---

Review: $ARGUMENTS

Detect the stack from the codebase and delegate to the matching reviewer subagent:

- Magento 2 -> magento-reviewer
- Laravel -> laravel-reviewer
- Pure PHP -> php-reviewer
- React -> react-reviewer
- Vue.js -> vue-reviewer

## Stack detection (path-first)

1. If `$ARGUMENTS` contains a filesystem path, resolve the nearest project manifest from that path (`package.json`, `composer.json`, `app/etc/config.php`) and detect from there before scanning the repo root.
2. Prefer the most specific match from the heuristics below.
3. If multiple stacks appear (monorepo / mixed — e.g., Laravel + Vue, or a PHP backend with a JS frontend) and the path does not clearly belong to one package, ask which subsystem to review.
4. If the stack is still not obvious, ask before proceeding.

Heuristics:
- Magento 2: `composer.json` requires `magento/framework` or `magento/module-*`, or `app/code` / `app/etc/config.php` present
- Laravel: `composer.json` requires `laravel/framework`, or typical `artisan` + `app/` + `routes/` layout
- Pure PHP: PHP project without Magento or Laravel framework markers
- React: nearest `package.json` requires `react`/`react-dom` or a React metaframework (`next`, `remix`, `gatsby`), or Vite with `@vitejs/plugin-react`. Do not treat bare `.tsx`/`.jsx` alone as sufficient when another UI library is indicated.
- Vue.js: nearest `package.json` requires `vue`/`@vue/*` or `nuxt`, or `.vue` SFCs under the resolved package path

The reviewer never modifies files. It must check the code against the project coding standards in `.coding-standards/`, prioritize security and performance issues, report each issue with severity, location, description and suggestion, and hand actionable findings to the matching `*-developer`. Test strategy and coverage planning belong to the matching `*-qa`.
