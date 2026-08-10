# PSR-4 — Autoloading Standard

This is the project reference for PSR-4, the autoloading standard. Every package in this project MUST follow PSR-4 autoloading.

## Core rule

The fully qualified class name of a class or interface MUST follow this structure for autoloading:

```
\<NamespaceName>(\<SubNamespaceNames>)*\<ClassName>
```

The term "class" refers to classes, interfaces, traits and other similar structures.

## Mapping rules

1. A fully qualified class name has two parts:
   - A **prefix** (the top-level namespace or a fully qualified vendor namespace). For example `App` or `Vendor\Package`.
   - A **relative class name** — everything after the prefix, which may include one or more sub-namespaces.

2. The prefix is mapped to a **base directory**:
   - `App\` → `/path/to/src/`
   - `Vendor\Package\` → `/path/to/package/src/`

3. The **relative class name** is mapped to a file path:
   - Each namespace separator `\` is converted to a directory separator `/`.
   - The class name (underscores are NOT meaningful for autoloading) is appended with the `.php` extension.
   - In every sub-namespace there MUST NOT be underscores converted to directory separators (unlike PSR-0).

## Examples

| Fully qualified class name | Namespace prefix | Base directory | Resulting file path |
|---------------------------|------------------|----------------|---------------------|
| `App\Domain\User` | `App\` | `./src/` | `./src/Domain/User.php` |
| `App\Infrastructure\Db\MysqlConnection` | `App\` | `./src/` | `./src/Infrastructure/Db/MysqlConnection.php` |
| `Vendor\Package\Service\Payment` | `Vendor\Package\` | `./packages/package/src/` | `./packages/package/src/Service/Payment.php` |

## composer.json configuration

PSR-4 is declared in `composer.json` under the `autoload` and `autoload-dev` keys:

```json
{
  "autoload": {
    "psr-4": {
      "App\\": "src/"
    }
  },
  "autoload-dev": {
    "psr-4": {
      "App\\Tests\\": "tests/"
    }
  }
}
```

### Rules

- The prefix MUST end with `\\` (double backslash) in JSON.
- Multiple namespaces MAY map to the same directory.
- The base directory is relative to the `composer.json` location.
- Test namespaces MUST map to a `tests/` directory separate from `src/`.

## Directory and file requirements

- One class per file.
- The class name MUST match the file name exactly (`User.php` contains `class User`).
- The directory structure MUST mirror the namespace exactly.
- File names are case-sensitive on most filesystems; the namespace case MUST match the directory case exactly.
- The file MUST declare `declare(strict_types=1);` and the namespace matching its path.

## Autoloader optimization

- Composer classmap authoritative mode (`composer dump-autoload -o --classmap-authoritative`) MUST be used in production.
- `--no-dev` MUST be used on deploy so dev autoloading (tests) is not installed.

## Validation

- Run `composer dump-autoload` after adding or renaming classes.
- Run `composer validate` to validate the `composer.json`.
- Run static analysis (PHPStan/Psalm) configured with PSR-4 paths to catch mismatches.
