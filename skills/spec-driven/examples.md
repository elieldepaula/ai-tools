# Spec-Driven Example: Order Splitting

User request:

```text
We need to allow a single quote to generate multiple orders
based on the customer's business unit.
```

## What the agent should do

1. Classify as a non-trivial (likely **Large** or **Medium**) Feature — do not start coding.
2. Search the repo for existing quote/order behavior and any prior specs.
3. Detect missing business decisions (how units partition, payment/invoice rules, etc.).
4. Run `grilling` for unresolved business decisions; write answers into the spec.
5. Create `specs/order-splitting/` (or `specs/COM-102-order-splitting/` if ticket-linked).
6. **Medium or Large**: delegate to the `*-architect` (e.g. `magento-architect`) to fill `spec.md`, `acceptance.md`, `architecture.md`, and `tasks.md` from templates — do not write the architecture yourself.
7. Identify Task dependencies; implement only after READY.
8. Implement per Task, loading context in order (load context → implement → test → completion report). **Large**: delegate each Task to a `*-developer`, independent Tasks in parallel; **Medium**: implement Tasks inline.
9. **Delegate validation to the `*-qa`** (test plan + execution evidence) and a final readonly review to the `*-reviewer`. Feature DONE only after all Tasks, acceptance, spec, architecture, QA, and review.

## Ambiguity example

```text
AMBIGUITY DETECTED

Question:
Should products without a collection be allowed when the quote
already contains products with a collection?

Possible interpretations:
A. Allow the product.
B. Reject the product.
C. Allow only when...
```

Then invoke `grilling`. Do not silently pick A/B/C.

## Resulting structure

```text
EPIC: Multi-Order Commerce
└── FEATURE: Order Splitting
    specs/order-splitting/
    ├── spec.md
    ├── architecture.md
    ├── acceptance.md
    ├── tasks.md
    └── tasks/
        ├── TASK-001-quote-partitioning.md   # Quote partitioning
        ├── TASK-002-order-creation.md       # Order creation
        ├── TASK-003-payment-allocation.md   # Payment allocation
        ├── TASK-004-invoice-generation.md   # Invoice generation
        └── TASK-005-integration-tests.md    # Integration tests
```

## Sample dependency order

```text
TASK-001 → TASK-002 → (TASK-003 ∥ TASK-004) → TASK-005
```

## Sample acceptance criterion

```text
Given a quote containing products from collection 2026
When the customer attempts to add a product from collection 2025
Then the product must not be added to the quote
And the customer must receive the defined business validation message.
```
