# Magento Coding Standard

This is the project reference for the Magento coding standard, applied on top of PSR-12. It is based on the official Magento Coding Standards and covers the conventions every Magento 2 module in this project MUST follow.

## Code style

- PHP style follows PSR-12 with Magento extensions: 4 spaces indentation, no tabs.
- Classes use PSR-4 autoloading (`Vendor_Module` namespace form: `Vendor\Module\...`).
- Every file MUST declare `declare(strict_types=1);` where PHP 8 is used consistently.
- Lines SHOULD NOT exceed 120 characters.

## Naming conventions

| Item | Convention | Example |
|------|-----------|---------|
| Module | `Vendor_Module` | `Acme_Catalog` |
| Namespace | `Vendor\Module\...` | `Acme\Catalog\Model\Product` |
| Classes | PascalCase | `Product`, `PriceCalculator` |
| Interfaces | PascalCase | `ProductRepositoryInterface` |
| Methods | camelCase | `getPrice()`, `saveProduct()` |
| Constants | UPPER_SNAKE_CASE | `STATUS_ENABLED` |
| Properties | camelCase | `$productRepository` |
| DB columns | snake_case | `sku`, `created_at` |
| Templates | kebab-case | `product/listing.phtml` |
| XML config | snake_case attributes, kebab file names | `di.xml`, `module.xml` |

## Directory structure

Every module MUST follow the Magento 2 canonical structure:

```
Vendor/Module/
├── Api/                    # Service contracts (interfaces)
│   └── Data/               # Data interfaces (DTOs)
├── Block/                  # Blocks
├── Controller/             # Controllers
├── Cron/                   # Cron jobs
├── etc/
│   ├── adminhtml/          # Admin configuration
│   ├── acl.xml             # Access control lists
│   ├── config.xml          # Module configuration
│   ├── di.xml              # Dependency injection
│   ├── events.xml          # Event/observer registration
│   ├── frontend/           # Frontend configuration
│   ├── module.xml          # Module declaration
│   ├── webapi.xml          # REST/SOAP API configuration
│   └── routes.xml          # Route configuration
├── Helper/                 # Helpers (only presentation/data helpers)
├── Model/                  # Models
│   ├── ResourceModel/      # Resource models
│   └── ResourceModel/…/Collection.php
├── Observer/               # Observers
├── Plugin/                 # Plugins (interceptors)
├── Setup/                  # Setup scripts (Install/Upgrade Schema/Data)
├── Test/                   # Tests
├── Ui/                     # UI components data providers, etc.
├── View/
│   ├── adminhtml/          # Admin templates/layouts
│   └── frontend/           # Frontend templates/layouts
├── ViewModel/              # View models
├── registration.php        # Module registration
└── composer.json           # Composer configuration
```

## Architecture rules

- **Service contracts first**: public functionality is exposed through `Api/` interfaces implemented by repositories. Controllers, CLI commands and other modules depend on contracts, never on concrete models.
- **Dependency injection**: all dependencies come through constructor injection via `di.xml`. `ObjectManager::getInstance()` is forbidden (see `Never-use-ObjectManager.md`).
- **Plugins over preferences**: extend behavior with plugins; preferences only for replacing broken/missing vendor logic (see `Plugins-over-Preferences.md`).
- **Declarative schema**: use `db_schema.xml` + `db_schema_whitelist.json` for new modules; setup scripts only for complex migrations.
- **No vendor changes**: vendor/ is read-only; use plugins, events, virtual types or composer patches (see `Never-modify-vendor.md`).
- **Lightweight observers**: observers dispatch work to queues or services; never heavy logic (see `Avoid-Heavy-Observers.md`).

## Frontend rules

- Blocks are presentation-only; business logic goes in ViewModels, services or repositories.
- Templates (.phtml) escape all output: `$block->escapeHtml()`, `escapeUrl()`, `escapeJs()`, `escapeHtmlAttr()`.
- Use Knockout/UI components for admin grids and forms.
- Use requirejs-config.js for module scripts; avoid inline JavaScript in templates.
- Layout handles (XML) define structure; do not inject logic via templates.

## Database rules

- Declarative schema for tables (`db_schema.xml`), always add foreign keys and indexes.
- Data access via collections and `addFieldToFilter`/`addAttributeToFilter`; never raw queries without bindings.
- Use `$searchCriteria` + repositories for public API access.
- Cache tags and cache types configured in `etc/cache.xml` for correct invalidation.

## Error handling and logging

- Log via `Psr\Log\LoggerInterface` (injected), never `echo`/`print_r`/`var_dump`.
- Throw specific exceptions: `LocalizedException` for user-facing messages, typed exceptions for technical errors.
- Use database transactions for atomic multi-step writes.

## Security rules

- CSRF: form keys on all admin forms and controllers (`_isAllowed` for admin routes, form key validation).
- ACL: every admin route and menu item requires an `acl.xml` entry.
- XSS: escape all output in templates; validate/sanitize input on controllers.
- SQL injection: always use bindings in queries.
- Never expose secrets in code or config; use `env.php`/environment variables and `config:set` with sensitive flags.

## Verification

- `vendor/bin/phpcs --standard=Magento2` for style compliance.
- `vendor/bin/phpstan analyse` for static analysis.
- `vendor/bin/phpunit` for the test suite.
- Deployment validates compilation: `bin/magento setup:di:compile`, `setup:static-content:deploy`.
