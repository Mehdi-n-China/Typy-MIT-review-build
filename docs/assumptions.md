# Assumptions and decisions

The specification leaves some things open. This page records every call that
was made, so it is easy to see what is a rule of the language and what is a
choice of this compiler. Change any of them deliberately, and update this page.

## Language

| Topic | Decision |
| --- | --- |
| Compiler-owned name | `__` (two underscores) is reserved and drives `repeat` (`for __ in range(n)`). A single `_` is an ordinary identifier. |
| What "reserved" means | A reserved word can never be *defined* (assigned, used as a parameter, loop target, function or class name, import alias, capture). Referencing one is allowed, so Python's builtin `any(...)` still works. |
| `self` | Parameters always need a type, including `self`; write `dyn self`. No implicit exemption was invented. |
| Async functions | `def` is not Typy, so `async TYPE name(...):` declares an async function. Without it `async` could not be used at all. |
| Variadic parameters | `*int values` / `**str opts` follow Python's annotation meaning: the type is that of each element. |
| Parameter defaults | The literal check applies to defaults too (`int f(int x = 1.5)` is an error). |
| `unless` / `until` | They negate the whole condition: `unless a or b` is `if not (a or b)`. |
| `else` on Typy loops | `until`, `forever`, `repeat` and initialized loops accept `else:` with Python's meaning. |
| Initialized loops | Loop variables are `dyn`, created before the first test and deleted in a `finally`. A variable of the same name that existed before is replaced and then deleted: these are throwaway variables. |
| Optional chaining | A `None` before a guarded step skips the whole rest of the chain. `?` attaches only to `.` and `[` (no `?(`), a trailing `?` is an error, and a chain cannot be assigned to or deleted. |
| `match` | A soft keyword: a line is only a `match` statement if Python would parse it as one; `match = ...` stays an assignment. |
| `type X = ...` | Parsed as a typed declaration of a variable of type `type`, not as Python 3.12's type alias statement. |
| Python-style annotations | `x: int = 5` behaves like `int x = 5`, including enforcement. |

## Type checking

| Topic | Decision |
| --- | --- |
| Exactness | Every check is `type(value) is expected`. `bool` is not `int`; subclasses never satisfy a parent. |
| `any` with a literal | The type is known at compile time, so the binding is resolved right away and enforced like a declaration of that type. Otherwise it is established at runtime by the first value. |
| Return values | With `--enforce`, every `return` is checked and so is falling off the end of a function (an implicit `None`). Generators are not return-checked. `void`, `any` and `dyn` returns are not checked. |
| Augmented assignment | `x += v` re-checks `x` afterwards. |
| Cross-file checks | Each file is compiled on its own; `void` misuse is only detected for functions declared in the same file. |
| Generated names | Helpers such as `_typy_ch1` and `_typy_state_1` skip any identifier already used in the file. |

## Builds

| Topic | Decision |
| --- | --- |
| Shorthand | `typy <target>` means `typy build <target>`, as the specification's `typy program.typy` / `typy project/` examples require. |
| Removed commands | `check`, `run` and `clean` are gone (2.2.0): build to check, run the output with Python, rebuild with `--override` to clean. |
| Excluded files | The *top-level* `output/` only (a nested folder called `output` is ordinary source), hidden files and folders, `__pycache__`, `.pyc` files, `.typyignore` and what it excludes. |
| Name clashes | `util.py` next to `util.typy` is an error instead of one overwriting the other. |
| Atomic builds | Everything is compiled before anything is written; output is staged in a temporary folder and published last. |
| Single files | Output goes to `output/` next to the file. |
| Entry point | `__main__.typy`, else `main.typy`, at the project root. Required by `--standalone`. |
| `--standalone` | Uses `zipapp`: one executable `.pyz` in `output/` and nothing else. A Python interpreter is still needed to run it. |
| `--bytecode` | Compiled files become `.pyc`; the runtime stays as source; no `__init__.py` markers are added (folders import as namespace packages). |
| `--gui` | A build flag. It only does something with `--enforce` (otherwise it is ignored with a note). The monitor is text-mode, on stderr; a graphical front-end can attach to the same runtime hook. |
| `--notify` | Three bells one second apart. One time in 69 it opens `assets/rickroll.mp4` with the system's default player instead, falling back to the bells if that fails. |
| `.typyignore` | Uses `pathspec`, which is therefore a required dependency. |

## Self-hosting

| Topic | Decision                                                                                                                                                                                                                                                          |
| --- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Layout | The compiler's Typy sources live in `../source/`, mirroring the package; the package's `.py` files are their compiled form and are committed, so `python -m Typy` works without a separate build step.                                                            |
| Rebuilding | `python -m typy.bootstrap` (written in Typy itself) recompiles the sources; `--check` verifies the package is a fixpoint. The test-suite runs that check.                                                                                                         |
| Generated Python | Keeps docstrings, loses comments (`ast` has no comments). The sources are what people read and edit.                                                                                                                                                              |
| Types in the sources | Parameters and variables are `dyn` unless a scalar literal shows the type (`int depth = 0`, `bool lightweight = False`); return types are `dyn`, or `None` for functions that return nothing. Building the compiler with `--enforce` passes the whole test-suite. |
| `__version__.version` | The version string is `version`, not `typy`: `typy` is a reserved word, so Typy code cannot define it.                                                                                                                                                            |
| Hand-written Python | `bootstrap/_stage0.py` (historical) and the test-suite (it must work even when the compiler does not).                                                                                                                                                            |

## Projects and data

| Topic | Decision                                                                                                          |
| --- |-------------------------------------------------------------------------------------------------------------------|
| `.typyexp` | A zip with a JSON manifest holding a SHA-256 per file; see [archive format](archive-format.md).                   |
| `typy import --override` | Replaces the destination folder entirely, but only after the whole archive has been verified.                     |
| Stats location | `typy/stats/` beside the package, or `TYPY_STATS_DIR`. Log files are only created when there is something to log. |
| Source files | Read as UTF-8 (a BOM is ignored); any newline style is accepted.                                                  |
| Python version | 3.14 or newer. Might work for lower versions but not supported.                                                   |
