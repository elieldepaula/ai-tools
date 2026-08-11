# Explain Architectural Decisions

Every significant architectural decision MUST be documented in a Decision Record (ADR) in this project. Code changes that implement a decision reference the ADR.

## Why

- Teams forget *why* a decision was made; months later the code looks wrong and gets "simplified" into a worse state.
- Undocumented decisions get re-litigated repeatedly, wasting review time.
- ADRs preserve context (alternatives considered, tradeoffs, constraints) that code cannot express.
- Onboarding is faster: new developers read the records instead of reverse-engineering the codebase.

## When an ADR is required

Create a decision record when a decision:
- Affects the architecture or public contracts (module boundaries, service contracts, preferences, virtual types).
- Introduces a new pattern or library that will be reused (queue topology, caching strategy, repository vs. collections).
- Is a hard rule exception (a preference where a plugin was expected — see `Plugins-over-Preferences.md`).
- Has meaningful tradeoffs and alternatives that were considered.
- Is expensive to reverse.

Minor decisions (naming, style, one-off bug fixes) do not need an ADR.

## ADR structure

ADRs live under `docs/adr/` named `NNNN-title.md` (e.g. `0001-use-message-queue-for-order-notifications.md`).

```markdown
# ADR-0001: Use message queue for order notifications

## Status
Accepted (2026-08-10)

## Context
Orders with 50+ items and three email templates caused checkout timeouts. Emails were sent synchronously in observers.

## Decision
Publish an `order.submitted` message to the RabbitMQ queue and consume it asynchronously. Observer only dispatches the message.

## Alternatives considered
- Cron job scanning orders: rejected — adds latency and unbounded polling.
- Direct async send (curl in background): rejected — no retry, no ordering.
- Plugin on order save: rejected — already covered by event, added coupling.

## Consequences
- Positive: faster checkout, retryable sends, decoupled from request lifecycle.
- Negative: email latency of a few seconds, queue required in deployments, monitoring needed.

## References
- `.coding-standards/Avoid-Heavy-Observers.md`
- `app/code/Acme/Sales/etc/queue_consumer.xml`
```

## Rules

- **Status + date** at the top; use `Proposed`, `Accepted`, `Deprecated`, `Superseded by ADR-NNNN`.
- **Context before decision**: always capture the problem and constraints first.
- **Alternatives considered**: at least one real alternative with reasons for rejection.
- **Consequences**: both positive and negative.
- **References**: link the affected code and related standards.
- Review ADRs with the same rigor as code; they are part of the codebase.

## Enforcement

- PRs that change module boundaries, contracts or introduce new patterns MUST include or link an ADR.
- Code review blocks merges of non-trivial architectural changes without a decision record.
