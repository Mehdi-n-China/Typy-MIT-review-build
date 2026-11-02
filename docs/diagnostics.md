# Diagnostics

Every error Typy reports on purpose is a `TypyBaseError`. On the command line
it prints as:

```text
error: <file>:line-<N>:col-<M>: <message>
  hint: <how to fix it>
```

Lines are 1-based, columns are shown 1-based. Errors that are not about source
code (an existing `output/`, a flag clash) print the bare message.

## Error classes

| Class | Raised for |
| --- | --- |
| `TypySyntaxError` | Malformed Typy: bad headers, misplaced clauses, `def`, missing values |
| `TypyIndentationError` | Tabs, missing or unexpected indented blocks |
| `TypyChainError` | Misused `?.` / `?[` |
| `TypyReservedIdentifierError` | A reserved word used as a name |
| `TypyUndeclaredVariableError` | Assigning a name that was never declared |
| `TypyTypeMismatchError` | A literal that does not match its declared type |
| `TypyVoidError` | A `void` function returning, or its result being used |
| `TypyCompilationError` | Several of the above, collected from one file or build |
| `TypyFlagConflict` | `--bytecode` with `--standalone` |
| `TypyNotAllowedToOverride` | Existing output without `--override` |
| `TypyProjectError` | Missing target, no `.typy` files, no entry point, name clashes |
| `TypyArchiveError` | Damaged, unsafe or invalid `.typyexp` files |
| `TypyInternalError` | A bug in Typy itself (please report it) |

Syntax errors stop at the first problem, since the rest of the file cannot be
trusted. Semantic errors are all collected and reported together, sorted by
position. A build compiles every file before reporting, so one run lists the
problems of the whole project.

Runtime failures under `--enforce` raise `TypyTypeError` from the runtime,
not one of the classes above.

## Common errors

| Message | Fix |
| --- | --- |
| `'x' is not declared` | Declare it first: `int x = ...` or `dyn x = ...`. |
| `'def' is not valid Typy` | Write a typed signature: `int add(int a, int b):`. |
| `a typed declaration needs a value` | `int x` alone is not allowed; give it a value. |
| `type mismatch: 'x' is declared int but its value is a float literal` | Types are exact: use `float x = 1.5` or `int x = 1`. |
| `every parameter needs a type before its name` | `int f(x)` -> `int f(dyn x)`; methods need `dyn self`. |
| `'f' is declared void; its result cannot be used as a value` | Call it on its own line, or give it a return type. |
| `invalid use of '?'` | `?` must be glued to `.` or `[`: `a?.b`, `a?[0]`. |
| `'__' is reserved` | `__` drives `repeat`; use `_` or a real name. |

## Logs

Every error is also written to the crash log under `typy/stats/logs/`
(created on the first message of a run), which is handy for post-mortems.
