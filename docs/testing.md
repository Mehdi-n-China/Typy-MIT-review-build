# Testing

The suite uses only the standard library's `unittest`. From the folder that
contains `Typy/`:

```bash
python -m unittest discover -s typy/tests -t .
```

The tests are plain Python on purpose: they must keep working when a change
to the Typy sources has broken the compiler.

Importing the test package points the logger at a temporary directory, so test
runs never write into `typy/stats/`. Notification tests mock the player and the
bell, so nothing plays during a test run.

| File | Covers                                                                          |
| --- |---------------------------------------------------------------------------------|
| `test_lexer.py` | Logical lines, tabs, delimiters, normalisation                                  |
| `test_parser.py` | Node shapes, locations, every statement form, syntax errors                     |
| `test_declarations.py` | Declarations, literals, the declare-before-assigning rule                       |
| `test_functions.py` | Signatures, markers, variadics, `void` / `None`, methods                        |
| `test_control_flow.py` | `until`, `forever`, `repeat`, `unless`, initialized loops                       |
| `test_optional_chaining.py` | Short-circuiting, laziness, invalid uses                                        |
| `test_reserved.py` | Reserved words                                                                  |
| `test_enforcement.py` | Every runtime check, generated import placement                                 |
| `test_codegen.py` | Shape of the generated Python: spacing, imports                                 |
| `test_stress.py` | `fixtures/stress.typy`, a large mixed program, run with and without `--enforce` |
| `test_build.py` | Real builds in temporary folders, run in a subprocess                           |
| `test_archive.py` | Export/import round trips, tampering, zip slip                                  |
| `test_cli_misc.py` | `version`, `stats`, the build shorthand                                         |
| `test_notifications.py` | The beep and its 1-in-69 alternative                                            |
| `test_fstrings.py` | Generated f-strings: same values as Python.                                     |
| `test_self_hosting.py` | The package is exactly its Typy sources compiled by itself                      |
| `test_changelog.py` | Release history vs schedule, version, registry and `Since:` notes               |
| `test_structure.py` | House rules on the Typy sources and the generated modules                       |

Helpers live in `tests/_support.py`: `compile_ok`, `compile_errors`,
`run_typy` (compile and execute), `run_cli` (run a command in-process and
capture its output) and `make_project` (a temporary project from a dict).
