# Never use ObjectManager

This is a HARD RULE in this project. The `ObjectManager` (`Magento\Framework\ObjectManagerInterface` and its static alias `ObjectManager::getInstance()`) MUST NOT be used to obtain objects.

## Why

- It hides dependencies: classes that call `ObjectManager::getInstance()` cannot be tested in isolation; the dependency graph is implicit.
- It breaks the service contract and DI model of Magento 2: instances are resolved at runtime instead of being injected.
- It is the root cause of hard-to-debug issues (shared instances, wrong lifecycle, hidden configuration).
- Magento's own rules (Magento Coding Standard, `Magento2.Functions.ObjectManager`) flag it as an error.

## Forbidden patterns

```php
// FORBIDDEN — never do this
$model = ObjectManager::getInstance()->get(\Vendor\Module\Model\Foo::class);
$helper = $this->_objectManager->get(Helper::class);
$objectManager = \Magento\Framework\App\ObjectManager::getInstance();
```

## Correct patterns

### Constructor injection (default)

```php
final class SomeService
{
    public function __construct(
        private readonly FooFactory $fooFactory,
        private readonly LoggerInterface $logger,
    ) {
    }
}
```

Wired via `di.xml`:

```xml
<type name="Vendor\Module\Service\SomeService">
    <arguments>
        <argument name="fooFactory" xsi:type="object">Vendor\Module\Model\FooFactory</argument>
        <argument name="logger" xsi:type="object">Psr\Log\LoggerInterface</argument>
    </arguments>
</type>
```

### Generated factories and proxies

- Use generated `*Factory` classes (auto-created for models) instead of `ObjectManager::getInstance()->create()`.
- Use generated proxies (`di.xml` `<argument xsi:type="object">Foo\Bar\Baz</argument>` with `shared="false"`, or proxy classes) for lazy loading.

### CLI commands

Magento CLI commands receive their dependencies through the constructor:

```php
class HelloWorld extends Command
{
    public function __construct(
        private readonly FooRepositoryInterface $fooRepository,
    ) {
        parent::__construct();
    }
}
```

### Contexts where access is available

In controllers, blocks, observers and actions you MUST only use injected dependencies or the generated factory passed to your constructor — never the ObjectManager.

## Enforcement

- CI runs `vendor/bin/phpcs --standard=Magento2` which reports ObjectManager usage as a blocking error.
- Code review rejects any `ObjectManager` reference.
- Violations are treated as high/critical issues.
