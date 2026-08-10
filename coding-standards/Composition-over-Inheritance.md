# Composition over Inheritance

This is the project reference for the composition over inheritance principle. Prefer object composition and delegation over class inheritance. This is a HARD RULE in this project.

## The principle

> Classes should achieve polymorphic behavior and code reuse by containing instances of other classes (composition), not by inheriting from them.

## Why

- Inheritance couples a class to its parent forever; a change in the parent silently changes every child.
- Inheritance exposes the parent's internals; composition exposes only what the class wants to expose.
- Multiple inheritance is impossible in PHP; composition has no such limit.
- Composition is easier to test (dependencies are injected and mockable).
- Deep inheritance hierarchies are hard to understand and refactor.

## Rules

### Preferred
- Extract shared behavior into small interfaces and delegate to injected collaborators.
- Use interfaces (`PaymentGateway`, `Notifier`, `LoggerInterface`) and inject concrete implementations.
- Use the Strategy pattern to swap behavior.
- Use the Adapter pattern to wrap external services and vendor classes.
- Use the Decorator pattern to add behavior without changing the object.
- Constructor injection is the ONLY way to obtain collaborators.

### Prohibited
- Class hierarchies deeper than one parent level (grandchild classes).
- "Helper" base classes whose only purpose is sharing utility methods (use traits or plain functions instead).
- Overriding methods to block the parent (`throw new LogicException` in an override — this also breaks LSP).
- Subclassing vendor/framework classes for convenience; wrap them instead.
- God base classes accumulating behavior for all descendants.

### Discouraged
- Deep inheritance for code reuse. Prefer delegation.
- `extends` where the relationship is "has a" instead of "is a".

## When inheritance IS acceptable

- A true "is a" relationship with behavior that will not change (e.g. an abstract base implementing a shared interface skeleton).
- The parent is abstract and defines a contract, children only implement specific steps (template method) — but prefer strategy when in doubt.
- Never more than two levels deep.

## PHP specifics

- Prefer interfaces + constructor promotion:

```php
interface PaymentGateway
{
    public function charge(float $amount): Receipt;
}

final class StripeGateway implements PaymentGateway
{
    public function charge(float $amount): Receipt
    {
        // ...
    }
}

final class CheckoutService
{
    public function __construct(
        private readonly PaymentGateway $paymentGateway,
        private readonly Notifier $notifier,
    ) {
    }
}
```

- Traits are allowed for pure, stateless behavior sharing, but composition is preferred when state is involved.
- `final` classes are the default; only make a class non-final when it is explicitly designed for extension.

## Enforcement

- Static analysis flags inheritance depth greater than 2.
- Code review flags any new `extends` outside an abstract contract base.
- New behavior MUST be added via new implementations or decorators, never by editing a shared parent.
