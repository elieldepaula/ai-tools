# PSR-12 — Extended Coding Style Guide

This is the project reference for PSR-12, the extended coding style guide for PHP. It extends PSR-1 (basic coding standard) and PSR-2 (coding style guide) with modern PHP 8.x conventions.

## General rules

- Code MUST follow "one class per file" and "one namespace per file".
- Files MUST use `<?php` opening tag and MAY omit the closing tag.
- Files MUST use UTF-8 without BOM.
- Files MUST declare `declare(strict_types=1);` right after the opening tag, before any other statement.
- Files MUST use 4 spaces for indentation, never tabs.
- Lines MUST be no longer than 120 characters; hard limit of 80 is strongly recommended.
- There MUST NOT be trailing whitespace at the end of lines.
- There MUST NOT be more than one blank line consecutively.
- Files MUST end with a single newline.
- Each file MUST include a namespace declaration and SHOULD include a block comment documenting its purpose.

## Class and namespace structure

- `namespace` and `use` declarations MUST be in the order: namespace, then `use` statements, alphabetically ordered, followed by one blank line.
- `use` statements MUST NOT be grouped with `use function` or `use const`; each is a separate list.
- A single blank line MUST separate the block of `use` declarations from the rest of the file.
- Opening braces for classes, interfaces, traits and enums MUST go on the next line (Allman style).
- Closing braces MUST be on their own line.
- The `abstract` and `final` keywords MUST precede `class`.
- Class constants MUST be declared in `UPPER_SNAKE_CASE` unless declared `final public` with `private(set)` semantics, in which case they MAY use CamelCase.

## Properties, methods and visibility

- Every property and method MUST have an explicit visibility (`public`, `protected` or `private`); implicit public is prohibited.
- `abstract`, `final`, `static` and visibility order: `abstract|final` then `static` then visibility.
- Properties MUST NOT be initialized with null explicitly (omit the default).
- Methods MUST have a return type declaration; return `void` when nothing is returned.
- Methods MUST have type hints for every parameter where the type is known.
- Opening braces of methods MUST go on the next line.
- Constructor property promotion SHOULD be used for simple value assignment.

## Control structures

- One space after control structure keywords (`if`, `elseif`, `else`, `for`, `foreach`, `while`, `switch`, `try`, `catch`, `match`).
- Opening braces of control structures go on the SAME line.
- Each `elseif`/`else`/`catch` MUST be on the same line as the closing brace of the previous block.
- Parentheses of control structures MUST NOT have spaces inside: `if ($x)`, never `if ( $x )`.
- `match` expressions: conditions are comma-separated, arms separated by commas, default arm as `default =>`.
- Control structures MUST have braces; single-statement bodies MUST still use braces.

## Operators

- All binary and ternary operators MUST be surrounded by at least one space: `$a + $b`, `$x === $y`.
- Unary operators MUST NOT be separated from their operand: `++$i`, `!$flag`, `(int)$value`.
- The null coalescing operator `??` and nullsafe operator `?->` MUST be surrounded by the same spacing rules as other binary operators (spaces for `??`, none after `?->`).
- Arithmetic and assignment operators: one space on each side.

## Function and method calls

- No space between the function name and the opening parenthesis.
- One space after each comma.
- Argument lists MAY be split across multiple lines for readability; when split, the first argument starts on a new line and each argument on its own line.
- Trailing commas in multiline argument lists and parameter lists are REQUIRED.

## Anonymous functions and arrow functions

- One space after `function` and after the closing parenthesis.
- Use the `fn` arrow function syntax for single-expression closures.
- `use` clause: one space before and after `use`; variables separated by commas with trailing comma allowed.
- Explicit return type for closures is encouraged.

## Visibility rules

- Class, interface, trait and enum declarations MUST declare visibility for all members.
- `readonly` properties SHOULD be used for immutable data.
- `enum` cases MUST be declared before any methods or properties.
- `enum` cases MUST NOT have visibility modifiers (implicit public).

## Naming conventions

- Classes, interfaces, traits, enums: `PascalCase`
- Methods: `camelCase`
- Functions: `camelCase` (or `snake_case` per project preference — prefer `camelCase`)
- Constants: `UPPER_SNAKE_CASE`
- Properties and variables: `camelCase`
- Parameters: `camelCase`

## DocBlocks and comments

- DocBlocks MUST be aligned consistently and use `/** ... */` syntax.
- Line comments MUST use `//`; `#` is discouraged.
- DocBlock order: `@param` then `@return` then `@throws`.
- Native type hints take precedence over `@param`/`@return` annotations.
- Do not repeat the type in the DocBlock when a native type hint already declares it.
