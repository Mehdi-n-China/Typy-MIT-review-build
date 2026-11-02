# Contributing

## Where the code lives

The compiler is written in Typy. Edit the `.typy` files in `../source/`; the
`.py` files of the package are generated from them and are overwritten by
every rebuild. After a change:

```bash
python -m Typy.bootstrap          # repeat until it reports 0 modules changed
python -m typy.bootstrap --check  # must pass before committing
```

If you break the compiler badly enough that it cannot rebuild itself,
`git checkout` the generated `.py` files: they are the last good build.

## House rules

1. **At most two functions per module.** A module does one job; helpers go in
   their own private module. Small classes are fine. `tests/test_structure.py`
   enforces this on the Typy sources.
2. **Private modules, public packages.** Implementation lives in `_name.py`
   files; each package's `__init__.py` imports and exposes its public surface.
3. **Standard library through `tools`.** Compiler code writes `tools.path.Path`,
   `tools.json.load`, `tools.pyast.parse`, not a direct `import`. New stdlib needs
   get a facade file in `tools/` and an alias in `tools/__init__.py`. The
   runtime packages are the exception: they ship with compiled programs and
   import the standard library directly.
4. **Docstrings everywhere.** Every module and every function says what it does
   and why. Package docstrings end with `Since: X.Y.Z`, the release that
   introduced the package (checked against the changelog by the tests).
5. **Python 3.14 compatible.** Generated code must run on 3.14+, so newer
   `ast` features are reached through `getattr` (see `../source/parser/_try.typy`
   and `TryStar`); the tests check the shipped modules for 3.12-only syntax.
6. **Errors are typed.** Raise a `TypyBaseError` subclass with a location and,
   where it helps, a `hint`.

## Adding a language construct

Say Typy gains `loop N times:`. Every step is one small module:

1. **Node**: add `../source/tree/_loop_times.typy` with a `TypyStatement`
   subclass and export it from `../source/tree/__init__.typy`.
2. **Parser**: add `../source/parser/_loop_times.typy` with
   `tuple parse_loop_times(dyn ctx, list lines, int index, list decorators):`
   returning `(nodes, next_index)`; teach `_classify.typy` to recognise the
   line and register the parser in `_dispatch.typy`. Parse sub-expressions
   with `parse_python_expression` and bodies with `parse_body`.
3. **Semantics**: usually nothing; the generic walkers (`child_blocks`,
   `map_blocks`) already reach the new node's body. Add a check module only if
   the construct has rules of its own.
4. **Lowering**: add `../source/lowering/_loop_times.typy` returning plain Python
   nodes and register it in `../source/lowering/__init__.typy`.
5. **Rebuild**: `python -m typy.bootstrap` until it reports no changes.
6. **Tests and docs**: a test file, a section in the language reference, a line
   in `docs/ast.md`, an `Unreleased` changelog entry.

## Workflow

```bash
python -m typy.bootstrap && python -m typy.bootstrap --check
python -m unittest discover -s typy/tests -t .
python -m typy build typy/example_project --enforce --override
```

Keep generated output out of commits (`.gitignore` covers `output/`,
`__pycache__/` and the stats data).
