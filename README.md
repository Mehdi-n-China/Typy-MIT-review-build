# Typy

Typy is a Python-compatible language that compiles to Python. It adds explicit
types, compile-time checks for what can be known for certain, optional runtime
enforcement and a handful of conveniences. Everything else is Python.

```typy
class Counter:
    None __init__(dyn self, int start = 0):
        self.value = start

int total(*int values, int bonus = 0):
    return sum(values) + bonus

dyn counter = Counter()
repeat 3:
    counter.value += 1

unless counter.value > 10:
    print("small:", total(1, 2, 3, bonus=counter.value))

dyn settings = {"home": {"city": "Montreal"}}
dyn city = settings?.get("home")?["city"]
i(0) until i >= 3:
    print(i)
    i += 1
```

## Quick start

Requirements: Python 3.14+ and `pathspec` (`pip install -r typy/requirements.txt`).
Run Typy from the folder that **contains** this one:

```bash
python -m typy build typy/example_project --enforce
python typy/example_project/output
```

| Command | What it does |
| --- | --- |
| `typy build <file-or-folder>` | Compile into `output/` (`--enforce`, `--gui`, `--bytecode`, `--standalone`, `--lightweight`, `--veritasium`, `--notify`, `--override`) |
| `typy <file-or-folder>` | Shorthand for `typy build` |
| `typy export <folder>` | Package a project as a verified `.typyexp` archive |
| `typy import <file.typyexp>` | Unpack one back into a folder |
| `typy stats` | What Typy has done on this machine |
| `typy version [--modules]` | Version, interpreter, every module |

(`typy` stands for `python -m typy`.)

## What Typy adds

- Typed declarations `int x = 10` and a declare-before-assigning rule.
- Typed signatures `int add(int a, /, int b = 5, *, str c, **str rest):` in
  place of `def`, with `void` and `None` return types.
- `any` (type fixed by the first value) and `dyn` (anything, never checked).
- `unless` / `elunless`, `until`, `forever`, `repeat`, and initialized loops
  `i(0) while i < n:` whose variables disappear afterwards.
- Optional chaining: `a?.b`, `a?[k]`, lazily short-circuiting on `None`.
- `--enforce`: exact runtime checks of variables, parameters and return values,
  with a live monitor (`--gui`).

## Typy is written in Typy

The compiler's source code is the `.typy` files in [`source/`](source/), which
mirror the package layout. Every `.py` file of the package is generated from
them, by Typy itself:

```bash
python -m typy.bootstrap            # recompile source/ into the package
python -m typy.bootstrap --check    # verify the package is exactly what its sources compile to
```

Edit the `.typy` sources, never the generated `.py`. Details in
[`docs/architecture.md`](docs/architecture.md#self-hosting).

## Documentation

Everything is in [`docs/`](docs/README.md): the language reference, the type
system, every command and flag, the build system, the AST, the runtime,
diagnostics, architecture and contributing guidelines.
[`docs/assumptions.md`](docs/assumptions.md) records every decision the
specification left open. The release history is in [`CHANGELOG.md`](CHANGELOG.md).

## Layout

```text
typy/
├── __main__.py, __version__.py, compiler.py, pipeline.py, packaging.py
├── lexer/  parser/  tree/  semantics/  enforcement/  lowering/  codegen/
├── context/  formatting/  runtime/  builder/  ignore/  archive/
├── notifications/  errors/  logger/  registry/  tools/  cli/  bootstrap/
├── source/   the compiler's Typy sources (the .py files are compiled from them)
├── docs/  tests/  example_project/  assets/  stats/
└── CHANGELOG.md  README.md  requirements.txt
```

Each source module holds at most two functions; see
[`docs/contributing.md`](docs/contributing.md) for the house rules.

## Tests

```bash
python -m unittest discover -s typy/tests -t .
```
