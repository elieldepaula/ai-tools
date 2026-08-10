# Plugins over Preferences

This is a HARD RULE in this project. Prefer **plugins (interceptors)** to extend Magento behavior. Preferences MUST only be used when plugins are technically impossible.

## Why

- Plugins decorate the original class: the core logic remains, is upgraded safely, and is still used.
- Preferences replace the whole class: your implementation must replicate 100% of the original behavior or it silently breaks, and upgrades can change the interface contract.
- Plugins compose; preferences fork. Multiple preferences for the same type cause a runtime error.
- Plugins are unit-testable in isolation (before/around/after hooks).

## Plugin patterns

```xml
<type name="Magento\Catalog\Api\ProductRepositoryInterface">
    <plugin name="acme_product_repository_after" type="Acme\Catalog\Plugin\ProductRepositoryPlugin" sortOrder="10"/>
</type>
```

```php
final class ProductRepositoryPlugin
{
    public function afterSave(
        ProductRepositoryInterface $subject,
        ProductInterface $result,
    ): ProductInterface {
        // extend behavior after save, never re-implement save
        return $result;
    }
}
```

Rules for plugins:
- Use `before*` to validate/modify arguments, `around*` to wrap logic (rare, use sparingly), `after*` to react to results.
- Return the same types as the intercepted methods.
- Keep plugins small and single-purpose.

## When preferences ARE allowed

Preferences are acceptable ONLY when:

1. The class is **final** or cannot be intercepted by a plugin (e.g. classes instantiated with `new`, static methods, hardcoded instantiation in core).
2. The vendor implementation is **broken** and cannot be fixed with plugins/events/virtual types, and a composer patch is not feasible.
3. Swapping an entire service contract implementation where inheritance/interception does not apply (e.g. replacing a gateway client).

When a preference is required:
- Extend the original class (`extends`) instead of copying it, reusing untouched behavior.
- Document in the class DocBlock why a preference is necessary (link to ADR if applicable).
- Keep the preference in your module, never in vendor.

## Virtual types

Before reaching for a preference, consider a **virtual type** to reconfigure a class:

```xml
<virtualType name="AcmeCatalogProductRepository" type="Magento\Catalog\Model\ProductRepository">
    <arguments>
        <argument name="metadataPool" xsi:type="object">Acme\Catalog\Model\ResourceModel\MetadataPool</argument>
    </arguments>
</virtualType>
```

Virtual types keep the original class intact and only change arguments.

## Enforcement

- Code review rejects preferences that could be replaced by a plugin.
- Violations are treated as high/critical issues.
- Any new preference MUST include a justification comment referencing this rule.
