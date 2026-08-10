# Laravel Conventions

This is the project reference for Laravel-specific conventions. Every Laravel application and package MUST follow these conventions on top of the PHP standards (PSR-12, PSR-4, SOLID, Clean Architecture, Composition over Inheritance).

## Directory structure

```
├── app/
│   ├── Console/            # Artisan commands, kernel
│   ├── Enums/              # PHP enums
│   ├── Events/             # Event classes
│   ├── Http/
│   │   ├── Controllers/
│   │   ├── Middleware/
│   │   └── Requests/       # Form Requests
│   ├── Jobs/               # Queued jobs
│   ├── Listeners/
│   ├── Mail/               # Mailables
│   ├── Models/             # Eloquent models
│   ├── Notifications/
│   ├── Policies/
│   ├── Providers/          # Service providers
│   ├── Services/           # Domain/application services
│   └── Actions/            # Single-action classes (optional)
├── bootstrap/
├── config/
├── database/
│   ├── factories/
│   ├── migrations/
│   └── seeders/
├── public/
├── resources/
│   ├── css/
│   ├── js/
│   └── views/              # Blade templates
├── routes/
│   ├── web.php
│   ├── api.php
│   └── console.php
├── tests/
│   ├── Feature/
│   ├── Unit/
│   └── Browser/
├── artisan
├── composer.json
└── .env.example
```

## Naming conventions

| Item | Convention | Example |
|------|-----------|---------|
| Model class | Singular PascalCase | `User`, `OrderItem` |
| Table | Plural snake_case | `users`, `order_items` |
| Migration | `create_xxx_table`, `add_xxx_to_xxx_table` | `create_orders_table` |
| Controller | Plural PascalCase + `Controller` | `UsersController`, `OrderItemsController` |
| Form Request | Action + `Request` | `StoreOrderRequest`, `UpdateUserRequest` |
| Route resource | plural kebab/snake | `Route::resource('order-items', ...)` |
| Factory | Model + `Factory` | `UserFactory` |
| Seeder | Entity + `Seeder` | `UserSeeder` |
| Service | Domain concept | `OrderService`, `PaymentService` |
| Job | Action-oriented | `SendWelcomeEmail` |
| Event | Past tense action | `OrderShipped` |
| Listener | Same as event | `SendShipmentNotification` |

## Eloquent

### Models
- Use `HasFactory` trait; define relations, casts and scopes on the model.
- Set `$fillable` (or `$guarded`) on every model. Mass assignment protection is mandatory.
- Use `protected $casts` (or `casts()` method) for typed attributes; prefer `array`/enum casts.
- Accessors/mutators via `Attribute` (PHP 8.x): `protected function fullName(): Attribute`.
- Global scopes and local scopes MUST be named and registered explicitly (`booted()` + `addGlobalScope`).
- Do NOT put business logic in models; models describe data + relationships + casts. Move logic to services/actions.
- Do NOT call external HTTP, write files, or send emails from models.

### Relationships
- Declare relationships explicitly with return types (`BelongsTo`, `HasMany`, `BelongsToMany`, `MorphTo`, etc.).
- Name relationships by convention: `belongsTo` → singular, `hasMany` → plural.
- Add `withCount`/`withSum` when aggregates are needed instead of loading full relations.
- Use `eager loading` (`with()`) to prevent N+1; use `whenLoaded()` in API resources.

### Queries
- Prefer Eloquent/query builder over raw SQL; use bindings (`whereRaw(..., [..])`) when raw is unavoidable.
- Use `whereNull`, `whereBetween`, `whereIn` etc. instead of string concatenation.
- Respect indexes: add indexes in migrations for foreign keys and frequently filtered columns.
- Use `chunkById` or cursor for large data sets; never `->get()` on huge tables.

## Controllers and routing

- Controllers MUST be thin: parse request, validate via Form Request, call a service/action, return a response.
- Use `Route::resource` for CRUD; use `only`/`except` to limit routes.
- Use route model binding (`{user}` → `User $user`) instead of manual lookups.
- Prefer controllers with `__invoke` (single action) for non-CRUD endpoints.
- API responses use API Resources (`app/Http/Resources`) or `response()->json`.
- Web routes use `Route::view` or resource controllers; business logic NEVER in closures unless trivial.

## Form Requests and validation

- Every controller method with user input MUST receive a Form Request.
- Validation rules defined in `rules()`, authorization in `authorize()` (policies).
- Use `authorize()` to enforce permissions; return 403 when unauthorized.
- Use `prepareForValidation`/`after` hooks only for legitimate transformations.
- Never trust request data: validate, cast, then pass to services.

## Service container and facades

- Bind contracts to implementations in a service provider (`$this->app->bind(Contract::class, Implementation::class)`).
- Inject contracts/classes via constructor; avoid `app()` in business code.
- Facades are acceptable in delivery/setup code (controllers, commands); prefer dependency injection in domain/application logic.
- Service providers MUST register bindings/events/commands; no business logic.
- Never call `Auth`, `Cache`, `DB`, `Log` facades inside domain services without injecting abstractions — for domain code, inject the underlying service.

## Blade

- Use `{{ }}` for escaped output, `{!! !!}` ONLY for trusted content (never for user input).
- Keep templates simple: presentation only; business logic in controllers/services.
- Use components (`<x-alert />`), layouts and partials instead of duplicating markup.
- Use `@error`, `@auth`, `@can` directives; validate permissions with policies, not ad-hoc checks in templates.
- Use localization `@lang`/`__()`; never hardcode strings that need translation.

## Artisan and scheduling

- New commands via `php artisan make:command`; name commands verb-noun (`order:expire`).
- Scheduled tasks in `routes/console.php` with `Schedule`; never cron logic in controllers.
- Queue jobs for heavy/slow work; use `ShouldQueue` on listeners/notifications when appropriate.

## Testing

- Use Pest (preferred) or PHPUnit.
- Feature tests cover HTTP endpoints end-to-end with `RefreshDatabase`.
- Use factories + seeders for test data; `fake()` for external services (HTTP, mail, queue, storage).
- Unit tests target services/actions/domain logic without touching the database when possible.
- Database tests use separate test DB (SQLite in-memory or MySQL test schema).
- Every controller method MUST have at least one feature test (happy path + validation error + authorization denial).

## Security

- Mass assignment: `$fillable`/`$guarded` on all models; never pass entire request arrays to `create()`.
- XSS: `{{ }}` escaping in Blade; never render user input with `{!! !!}`.
- CSRF: keep `@csrf` in all POST/PUT/PATCH/DELETE forms; use `XSRF-TOKEN` header for SPA/API.
- SQL injection: bindings only; never concatenate input into queries.
- Auth: policies + gates for authorization; `auth()->user()` instead of manual checks.
- Rate limiting: `RateLimiter`/`throttle` on auth and public endpoints.
- Uploads: validate MIME/size, store in `storage/`, serve via storage link, never execute uploads.

## Performance

- Eager load relations; watch for N+1 in loops and API resources.
- Cache read-heavy queries with tags and short TTLs (`Cache::remember`).
- Offload emails/notifications/heavy computation to queues.
- Use `select` to limit columns when returning large datasets.
- Index foreign keys and frequently filtered columns.
- Use pagination (`paginate`/`cursorPaginate`) on all listing endpoints.
- Consider Octane/Horizon only when profiling justifies it.
