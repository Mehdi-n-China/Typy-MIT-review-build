# Typy documentation

Typy is a Python-compatible language that compiles to Python. It adds explicit
typing, limited compile-time checking, optional runtime enforcement and a few
syntactic conveniences, and otherwise behaves exactly like Python.

| Document | What it covers |
| --- | --- |
| [Getting started](getting-started.md) | Requirements, the first program, the first project |
| [Language reference](language-reference.md) | Every construct Typy adds, with the Python it becomes |
| [Type system](type-system.md) | Declarations, literals, `any` / `dyn` / `void` / `None`, `--enforce` |
| [Command line](cli.md) | Every command, flag and exit code |
| [Build system](build-system.md) | Targets, `output/`, `.typyignore`, bytecode, standalone, the monitor |
| [Archive format](archive-format.md) | The `.typyexp` files written by `typy export` |
| [Architecture](architecture.md) | The compiler pipeline, self-hosting and the package map |
| [The Typy AST](ast.md) | Every node class and how it lowers |
| [Runtime](runtime.md) | What compiled programs import, and the enforcement monitor |
| [Diagnostics](diagnostics.md) | Error classes, message format, common errors |
| [Contributing](contributing.md) | House rules for the code base, adding a language feature |
| [Testing](testing.md) | Running and extending the test-suite |
| [Release process](release-process.md) | Versioning, the release schedule, the changelog |
| [Assumptions](assumptions.md) | Every decision the specification left open, and how it was made |
| [FAQ](faq.md) | Short answers to the questions that come up first |

The release history lives in [`../CHANGELOG.md`](../CHANGELOG.md).
