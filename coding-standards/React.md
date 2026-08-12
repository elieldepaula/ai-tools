# React

This is the project reference for React. All React code MUST follow the rules below. Prefer the official [React docs](https://react.dev) and the [Rules of React](https://react.dev/reference/rules) when a rule here is silent.

## Naming conventions

| Item | Convention | Example |
|------|-----------|---------|
| Component | PascalCase | `UserCard`, `OrderList` |
| Component file | PascalCase | `UserCard.tsx` |
| Hook | `use` + PascalCase | `useAuth`, `useLocalStorage` |
| Utility / feature file | kebab-case | `format-currency.ts` |
| Props | camelCase | `userId`, `onSubmit` |
| Boolean props | `is*` / `has*` / `can*` | `isOpen`, `hasError` |
| Event callback props | `on*` | `onClose`, `onChange` |
| Constants | UPPER_SNAKE_CASE | `MAX_PAGE_SIZE` |
| Context | PascalCase + `Context` | `AuthContext` |
| Test file | co-located `*.test.tsx` / `*.spec.tsx` | `UserCard.test.tsx` |

## File structure

```
src/
├── components/          # shared, reusable components
├── features/            # feature-scoped modules (components + hooks + state)
├── hooks/               # shared custom hooks
├── lib/                 # utilities, API clients, formatters
├── pages/ or app/       # route components (Vite/CRA) or App Router tree (Next.js)
├── store/               # global state configuration (when applicable)
└── types/               # shared TypeScript types
```

Adapt to the metaframework in use (e.g. Next.js `app/` routes, Remix `app/routes`). Do not invent a parallel structure when the project already has one.

## Components and props

- Prefer function components over class components.
- One component per file by default; co-locate style and test with the component unless the project organizes differently.
- Props MUST be explicit and typed; never pass `any` or mutate props.
- Use `children` composition over prop drilling.
- Destructure props in the function signature.
- Keys MUST be stable and unique (`id`), never the array index when the list can change.

## Hooks

- Follow the Rules of Hooks: only call hooks at the top level, never inside loops, conditions, or nested functions.
- Only call hooks from React function components or custom hooks.
- Name custom hooks with the `use` prefix.
- Extract reusable logic into custom hooks instead of duplicating it.
- Dependency arrays MUST list every value the effect reads; do not disable the linter to suppress warnings.
- Effects MUST have cleanup when they subscribe, add event listeners, or start timers.
- Prefer deriving values at render time over syncing state from props/effects.
- Prefer modern primitives when the project supports them: `use`, `useEffectEvent`, `startTransition`, `useDeferredValue`.
- When the React Compiler is enabled, do not hand-roll `useMemo`/`useCallback`/`React.memo` by default — add them only when profiling still shows a need the compiler cannot fix.
- Without the React Compiler, use `useMemo`/`useCallback`/`React.memo` only when there is a measured reason; do not wrap everything.

## State management

- Prefer local state with `useState`/`useReducer` for state used by one component or its children.
- Lift state up only when several sibling components need it; prefer composition otherwise.
- Use Context for shared low-frequency data (theme, locale, auth); do not use it as a global store for frequently changing data.
- Use a dedicated state library (Zustand, Redux Toolkit, Jotai) only when the application state is genuinely global and complex.
- Selectors must be narrow: components must re-render only when the slice they read changes.

## Data fetching

- Prefer a data-fetching library (TanStack Query, SWR) over hand-rolled `useEffect` + `fetch` in client components.
- In Next.js App Router / RSC, prefer server-side data fetching and Server Actions for mutations when they fit the architecture; keep client caches for interactive client state.
- Server state MUST NOT be stored in global client stores; keep it in the data-fetching layer with cache, dedup, and invalidation.
- Handle loading, error, and empty states explicitly.
- Cancel/abort requests on unmount when not using a library that does it automatically.
- Never expose tokens or secrets in the client bundle; read them from the server.

## Forms

- Prefer schema-driven validation (Zod or equivalent) shared with the API when possible.
- Use a form library (React Hook Form or similar) for non-trivial forms; keep uncontrolled fields where it simplifies the model.
- Surface field and form-level errors accessibly (`aria-invalid`, `aria-describedby`, linked error text).
- Disable submit while pending; preserve user input on validation failure.

## Styling

- Follow the project’s established styling approach; do not introduce a second system without an architect decision.
- Prefer CSS Modules or Tailwind utility classes for app UI; reserve CSS-in-JS for cases the design system requires.
- Keep design tokens (color, spacing, type) centralized; avoid hard-coded one-off values on hot paths.
- Prefer semantic HTML and existing design-system components over custom styled one-offs.

## Metaframeworks (Next.js / Remix / similar)

- Respect the project’s router model (App Router vs Pages Router, Remix routes).
- Keep Server Components pure when using RSC: no browser-only APIs, no wrong-boundary hooks.
- Mark client entry with `"use client"` only where interactivity or browser APIs are required; push data work up to the server when possible.
- Do not ship secrets, privileged tokens, or server-only env vars into client bundles.

## Rendering and performance

- Split large components; the `children` prop is not affected by parent re-renders.
- Avoid inline object/array/function props on hot paths inside memoized trees (when memoization is in use).
- Virtualize long lists (react-window / @tanstack/react-virtual).
- Lazy-load routes and heavy components with `React.lazy` + `Suspense` (or framework route splitting).
- Keep bundle size in check: code-split by route, avoid large direct imports, use tree-shakeable imports.
- Profile before optimizing (React DevTools Profiler, Lighthouse).

## Accessibility

- Use semantic HTML (`button`, `a`, `label`, landmarks) before ARIA.
- Every interactive control MUST have an accessible name (label, `aria-label`, or labelledby).
- Modals and drawers MUST trap focus, restore focus on close, and be escapable with Escape.
- Manage focus on route changes and after async UI that opens new content.
- Do not rely on color alone; meet contrast expectations for text and controls.
- Prefer Testing Library queries by role/label to encode a11y in tests.

## TypeScript

- Type all props, state, and hook return values.
- Use `interface` for object props/shapes and `type` for unions and primitive aliases.
- Prefer `useState` with explicit typing when the initial value does not imply the type.
- Never use `as any`; use proper narrowing or `unknown` + guards.
- Event handlers must be typed (`React.ChangeEvent<HTMLInputElement>`, etc.).

## Lint and format

- Enable `eslint-plugin-react-hooks` (rules of hooks + exhaustive-deps) and keep it clean — do not disable without a documented reason.
- Prefer the project’s ESLint + Prettier (or Biome) config; do not fight the repo formatter.
- Typecheck in CI (`tsc --noEmit`) for application code.

## Security

- Never render user-controlled HTML with `dangerouslySetInnerHTML`; sanitize through a library when unavoidable.
- Escape all output by default; React escapes by default, do not bypass it.
- Validate and sanitize all external data before use.
- Never commit secrets, API keys, or tokens; load them from the server or environment.
- Guard against open redirects, prototype pollution, and insecure deserialization when parsing external data.
- Audit dependencies for known vulnerabilities (`npm audit`).

## Observability

- Use Error Boundaries around feature islands that can fail independently.
- Log client errors with enough context for triage; never log secrets or PII beyond what policy allows.
- Prefer structured feature flags over commented-out code paths.

## Testing

- Prefer React Testing Library for behavior-focused tests (query by role/text, not by implementation).
- Test user-visible behavior, not internals (no testing implementation details like class names).
- Cover happy paths, error/loading states, and edge cases.
- Use Vitest or Jest with Testing Library and `@testing-library/user-event`.
- Use Playwright or Cypress for end-to-end flows.
- Prefer MSW for API mocking in component/integration tests.

## Anti-patterns

| Avoid | Prefer |
|-------|--------|
| Class components for new UI | Function components + hooks |
| `useEffect` to sync props → state | Derive at render or lift state |
| Server data in Zustand/Redux | TanStack Query / SWR / RSC fetch |
| `any` / `as any` | Narrowing, generics, `unknown` |
| Index as `key` on dynamic lists | Stable ids |
| Disabling `react-hooks/exhaustive-deps` | Fix dependencies or extract events |
| Blanket `useMemo`/`useCallback` | Measure first; trust the Compiler when enabled |
| Secrets in `NEXT_PUBLIC_*` / client env | Server-only secrets |

## Violations to flag

- Class components where a function component suffices.
- Hooks called conditionally or inside loops.
- Stale dependency arrays or missing effect cleanup.
- `dangerouslySetInnerHTML` with unescaped/untrusted content.
- Server state in global stores instead of a data-fetching layer.
- Over-memoization without measured need (especially with React Compiler on).
- Missing accessible names, focus traps, or keyboard paths on interactive UI.
- Secrets, tokens, or API keys in client code.
