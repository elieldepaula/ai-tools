# Clean Architecture

This is the project reference for Clean Architecture. All packages MUST follow the dependency rule: source code dependencies point INWARD, toward the domain.

## The dependency rule

> Dependencies in source code always point toward the domain layer. Nothing in an outer circle can mention anything in an inner circle.

The layers, from innermost to outermost:

```
                     ┌─────────────────────┐
                     │    Entities /       │   ← No dependencies
                     │  Value Objects      │
                     └─────────────────────┘
                     ┌─────────────────────┐
                     │   Use Cases /       │   ← Depends only on domain
                     │   Domain Services   │
                     └─────────────────────┘
             ┌─────────────────────────────────┐
             │ Application (repositories,     │   ← Interfaces only
             │ port definitions, events)      │
             └─────────────────────────────────┘
     ┌─────────────────────────────────────────────┐
     │ Infrastructure (DB, HTTP, queue, mail)      │   ← Implements
     │                                              │     application ports
     └─────────────────────────────────────────────┘
┌───────────────────────────────────────────────────────────┐
│ Presentation / Delivery (HTTP handlers, CLI, templates)    │
└───────────────────────────────────────────────────────────┘
```

## Layer responsibilities

### Domain layer (`src/Domain/`)
- Entities: objects with identity and behavior; encapsulate invariants.
- Value objects: immutable, compared by value, validated on construction.
- Domain services: operations that do not fit a single entity.
- Domain events: facts that happened, expressed in domain language.
- MUST NOT import anything from infrastructure, framework, or vendor beyond language primitives.
- MUST NOT have any dependency on the database, HTTP, or the container.

### Application layer (`src/Application/`)
- Use cases / application services: orchestrate one business transaction.
- Ports: interfaces that the application needs (repositories, gateways, message producers). Defined here, NOT in infrastructure.
- DTOs: data passed between layers.
- MAY reference domain types; MUST NOT reference infrastructure types.
- Business rules from the domain are applied here; delivery and persistence are NOT.

### Infrastructure layer (`src/Infrastructure/`)
- Concrete implementations of ports: PDO repositories, HTTP clients, queue adapters.
- Third-party libraries and drivers live here and are adapted behind ports.
- MUST NOT contain business rules.
- Implements interfaces from the application layer (dependency inversion).

### Presentation/delivery layer
- HTTP handlers/controllers, CLI commands, middlewares, templates.
- Thin: only parse input, call an application use case, format output.
- MUST NOT contain business logic, SQL, or direct infrastructure calls.

## Rules

- The domain layer MUST have zero imports from outside `src/Domain/` except PHP core.
- The application layer MUST only import `Domain` and its own interfaces.
- Infrastructure and presentation MAY depend on application and domain.
- Dependency injection wiring lives in the composition root (bootstrap), never inside classes.
- Data crossing layers uses simple DTOs, not domain entities when possible, and never infrastructure objects.
- Business logic MUST be testable without a database or HTTP server (unit tests cover domain + application).

## Directory structure

```
src/
├── Domain/
│   ├── Entity.php
│   ├── ValueObject.php
│   ├── DomainEvent.php
│   └── Service.php
├── Application/
│   ├── UseCase.php
│   ├── Port.php              # interfaces (repositories, gateways)
│   └── Dto.php
├── Infrastructure/
│   ├── Pdo/
│   ├── Http/
│   └── Queue/
└── Presentation/
    ├── Http/
    └── Cli/
```

## Violations to flag

- Domain classes containing `use PDO;`, `use HttpClient;` or calls to `getenv()`/container.
- Use cases performing SQL or HTTP directly.
- Entities with methods that persist themselves (`$entity->save()`).
- Controllers containing business rules or SQL.
- Any import from an outer layer into an inner layer.
