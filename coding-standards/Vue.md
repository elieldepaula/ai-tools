# Vue

This is the project reference for Vue. All Vue code MUST follow the rules below. Prefer the official [Vue docs](https://vuejs.org) and the [Vue Style Guide](https://vuejs.org/style-guide/) (Priority A/B) when a rule here is silent.

## Naming conventions

| Item | Convention | Example |
|------|-----------|---------|
| Component name | Multi-word PascalCase | `UserCard`, `OrderList` (never single-word like `Card`) |
| SFC file | PascalCase matching the component | `UserCard.vue` |
| Composable | `use` + PascalCase | `useAuth`, `useLocalStorage` |
| Props (script) | camelCase | `userId`, `isOpen` |
| Props (template) | kebab-case | `user-id`, `is-open` |
| Emits | kebab-case, declared in `defineEmits` | `update:model-value`, `item-selected` |
| Pinia store id | kebab-case | `useUserStore` / id `'user'` |
| Constants | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE` |
| Directives / plugins | camelCase | `vFocus`, `installLogger` |
| Test file | co-located `*.test.ts` / `*.spec.ts` | `UserCard.test.ts` |

Follow Vue Style Guide Priority A: component names are always multi-word.

## File structure

```
src/
├── assets/              # static assets
├── components/          # shared, reusable components
├── composables/         # shared composables (use-prefixed)
├── layouts/             # layout components
├── router/              # router configuration (SPA)
├── stores/              # Pinia stores
├── utils/               # utilities, API clients, formatters
├── views/ or pages/     # route components
└── types/               # shared TypeScript types
```

Adapt to Nuxt (`app/`, `pages/`, `server/`, `layers/`) when that is the project layout. Do not invent a parallel structure when the project already has one.

## Single-File Components

- One component per `.vue` file by default.
- Prefer `<script setup>` (Composition API) over the Options API for new code.
- Order the SFC blocks: `<script setup>`, `<template>`, `<style>`.
- Keep templates simple: presentation only, no business logic.
- Use `<template>` slots for layout and composition over prop drilling.
- Legacy Options API code may remain until migrated; do not expand it — extract new logic into Composition API composables instead (use the caveman skill when navigating unmaintained Options code).

## Composition API

- Use `ref` for primitive state and `reactive` for object state; prefer `ref` when reassignment clarity matters.
- Prefer `computed` over method calls in templates for derived values.
- Use `watch`/`watchEffect` for side effects that follow reactive state; prefer `computed` when the goal is a derived value.
- Never mutate props; emit events or use `v-model` instead.
- Name composables with the `use` prefix and keep them in `composables/`.
- Always clean up global listeners, intervals, and observers in `onUnmounted`/`onBeforeUnmount`.
- Keep components small; extract reusable logic into composables.

## State management

- Use local component state by default.
- Use Pinia for global application state; avoid hand-rolled stores with reactive singletons.
- Keep stores focused: one concern per store, actions for mutations, getters for derived state.
- Do not store server state in Pinia when a data-fetching layer (TanStack Query/Vue Query, SWRV, or Nuxt `useAsyncData`/`useFetch`) fits better.
- Selectors/getters must be narrow so only the consuming components update.

## Data fetching

- Prefer Vue Query/TanStack Query, SWRV, or Nuxt data utilities over ad-hoc `onMounted` + `fetch` for shared server state.
- Handle loading, error, and empty states explicitly.
- Cancel or ignore stale requests on unmount when the library does not do it for you.
- Never expose tokens or secrets in the client bundle; read them from the server.

## Forms

- Prefer schema-driven validation (Zod or equivalent) with VeeValidate or similar when forms are non-trivial.
- Use `v-model` and typed emits for reusable form controls.
- Surface field and form-level errors accessibly (`aria-invalid`, `aria-describedby`, linked error text).
- Disable submit while pending; preserve user input on validation failure.

## Styling

- Follow the project’s established styling approach; do not introduce a second system without an architect decision.
- Prefer `<style scoped>` or CSS Modules for component CSS; Tailwind/UnoCSS when the project already uses them.
- Keep design tokens centralized; avoid hard-coded one-off values on hot paths.
- Prefer semantic HTML and existing design-system components over custom styled one-offs.

## Nuxt and metaframeworks

- Respect Nuxt conventions: file-based routing, `layouts/`, auto-imports, and `server/` API routes when present.
- Prefer `useAsyncData` / `useFetch` for SSR-friendly data; keep secrets and privileged work in `server/` or server utilities.
- Use Nuxt layers for shared product shells only when the monorepo already adopts them.
- Mark client-only code with `<ClientOnly>` or `.client` suffixes when browser APIs are required.

## Rendering and performance

- Use `v-show` for frequent toggles and `v-if` for conditional mounting.
- Do not use `v-if` together with `v-for` on the same element; use a computed filter.
- Set stable `:key` on `v-for` (id, not index) when the list can change.
- Lazy-load routes with dynamic imports and heavy components with `defineAsyncComponent`.
- Memoize large static trees with `v-memo` only when there is a measured benefit.
- Batch updates where possible and avoid deep reactive objects on hot paths.
- Avoid unnecessary watchers; prefer `computed` and explicit user actions.
- Profile before optimizing (Vue DevTools, Lighthouse).

## Accessibility

- Use semantic HTML (`button`, `a`, `label`, landmarks) before ARIA.
- Every interactive control MUST have an accessible name (label, `aria-label`, or labelledby).
- Modals and drawers MUST trap focus, restore focus on close, and be escapable with Escape.
- Manage focus on route changes and after async UI that opens new content.
- Do not rely on color alone; meet contrast expectations for text and controls.
- Prefer Testing Library queries by role/label to encode a11y in tests.

## TypeScript

- Use `<script setup lang="ts">` with typed `defineProps`/`defineEmits`.
- Type composable return values and Pinia state/actions.
- Never use `as any`; prefer proper narrowing or `unknown` + guards.
- Keep template refs typed (`Ref<HTMLInputElement | null>`).

## Lint and format

- Enable `eslint-plugin-vue` (essential / strongly-recommended) and keep it clean — do not disable without a documented reason.
- Prefer the project’s ESLint + Prettier (or Biome) config; do not fight the repo formatter.
- Typecheck in CI (`vue-tsc --noEmit` or equivalent) for application code.

## Security

- Never render user-controlled HTML with `v-html`; sanitize through a library when unavoidable.
- Escape all output by default; Vue escapes by default, do not bypass it.
- Validate and sanitize all external data before use.
- Never commit secrets, API keys, or tokens; load them from the server or environment.
- Guard against open redirects and prototype pollution when parsing external data.
- Audit dependencies for known vulnerabilities (`npm audit`).

## Observability

- Prefer app-level error handling (`app.config.errorHandler`, Nuxt error pages) around feature islands that can fail independently.
- Log client errors with enough context for triage; never log secrets or PII beyond what policy allows.
- Prefer structured feature flags over commented-out code paths.

## Testing

- Prefer Vue Test Utils for mount-level tests and Testing Library (`@testing-library/vue`) for behavior tests.
- Test user-visible behavior: rendered output, emitted events, v-model updates.
- Cover happy paths, error/loading states, and edge cases.
- Use Vitest for unit/component tests and Playwright or Cypress for end-to-end flows.
- Prefer MSW for API mocking in component/integration tests.

## Anti-patterns

| Avoid | Prefer |
|-------|--------|
| Options API for new features | `<script setup>` + composables |
| Business logic in templates | Computed, methods in script, or composables |
| Mutating props | Emits / `v-model` |
| `v-if` + `v-for` on same node | Computed filtered list |
| Index as `:key` on dynamic lists | Stable ids |
| Server data only in Pinia | Vue Query / `useAsyncData` / `useFetch` |
| `any` / `as any` | Narrowing, generics, `unknown` |
| Expanding legacy Options modules | Extract composables; migrate incrementally |
| Secrets in `NUXT_PUBLIC_*` / client env | Server-only secrets |

## Violations to flag

- Options API where Composition API is the project standard (for new or touched code).
- Business logic inside templates.
- Mutating props directly.
- `v-if` with `v-for` on the same element.
- Array index as `:key` on dynamic lists.
- `v-html` with unescaped/untrusted content.
- Unhandled listeners/intervals/observers left without cleanup.
- Missing accessible names, focus traps, or keyboard paths on interactive UI.
- Secrets, tokens, or API keys in client code.
