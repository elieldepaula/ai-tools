# SOLID Principles

This is the project reference for the five SOLID principles. Every class, interface and package in this project MUST comply with these principles.

## S — Single Responsibility Principle (SRP)

> A class should have only one reason to change.

### Rules
- A class MUST have one clearly defined responsibility.
- A class MUST have a name that describes its single responsibility.
- A class that mixes persistence, HTTP concerns and business logic violates SRP.
- Split responsibilities into: entities/value objects (state), services (behavior), repositories (persistence), handlers/controllers (transport).
- If a class has more than one method that can be described with different verbs, consider splitting it.

### Symptoms of violation
- God classes with many unrelated methods.
- A class that is changed for unrelated reasons.
- Long method lists touching many different concerns.

## O — Open/Closed Principle (OCP)

> Software entities should be open for extension, but closed for modification.

### Rules
- New behavior MUST be added by extending (new classes, new implementations, new strategies) — never by editing existing, tested code.
- Rely on interfaces and abstractions; add new implementations without touching existing ones.
- Prefer strategy pattern, decorator pattern, and interface polymorphism over `if/elseif` chains on type.
- Configuration and behavior switching MUST go through injected dependencies, not hardcoded conditionals.

## L — Liskov Substitution Principle (LSP)

> Subtypes must be substitutable for their base types without altering the correctness of the program.

### Rules
- A subclass MUST be usable anywhere its parent is expected.
- Preconditions MUST not be strengthened; postconditions MUST not be weakened.
- Overridden methods MUST accept the same or wider input and return the same or narrower output (covariance/contravariance).
- Methods MUST not throw new exceptions not declared/thrown by the parent contract.
- Do NOT override a method to throw `BadMethodCallException` or `LogicException` — this breaks LSP; use composition instead.

## I — Interface Segregation Principle (ISP)

> No client should be forced to depend on methods it does not use.

### Rules
- Interfaces MUST be small and focused on a single role.
- Split fat interfaces into role-specific ones (e.g. `PaymentGateway`, `Refundable` instead of one `PaymentProcessor`).
- A class implementing an interface MUST implement every method meaningfully; no empty method bodies.
- Prefer several small interfaces over one large interface.
- Consumers MUST depend only on the interface they need.

## D — Dependency Inversion Principle (DIP)

> High-level modules should not depend on low-level modules. Both should depend on abstractions.

### Rules
- Depend on interfaces and abstract classes, not concrete implementations.
- Inject dependencies via constructor; never instantiate dependencies inside classes (`new`, static factories).
- Domain and application layers MUST NOT reference infrastructure (database drivers, HTTP clients, filesystem).
- Infrastructure implementations MUST implement interfaces defined in the domain/application layer.
- Service locators, service containers reached from inside classes, and static facades are forbidden in business code.

## Enforcement in this project

- All dependencies are injected via constructor with interfaces as parameter types.
- Static analysis (PHPStan level max, Psalm) enforces interface usage.
- Repository contracts are defined in the domain layer; SQL/PDO lives in infrastructure.
- New feature requests result in new classes, not edits to existing ones (OCP).
