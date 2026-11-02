# Changelog

All notable changes to Typy. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and Typy uses
semantic versioning:

- a **MINOR** release (`x.Y.0`) ships something notable and lands on the regular
  schedule, the **15th of March, June, September and December**;
- a **PATCH** release (`x.y.Z`) is a fix or a small optimization. Scheduled
  quarters with nothing big to ship get one too; hotfixes go out whenever needed;
- a **MAJOR** release happens when it happens.

See [`docs/release-process.md`](docs/release-process.md) for the details.

## [Unreleased]

Next scheduled release: 2.4.0 on 2026-12-15.

## [2.3.9] - 2026-10-29

### Fixed

- `--enforce` no longer appends the "missing return" check after a function
  whose last statement already is a `return` or `raise` (it was dead code).
- Documentation: every package now names the release that introduced it.

## [2.3.8] - 2026-10-26

### Changed

- Names the compiler invents (`_typy_ch1`, `_typy_state_1`, ...) now skip any
  identifier already used in the file instead of trusting the prefix.

### Fixed

- `typy version --modules | head` no longer ends in a `BrokenPipeError` traceback.

## [2.3.7] - 2026-10-20 (hotfix)

### Fixed

- `--notify` reported the Rickroll as unavailable even after the player had
  launched, and the ordinary beep had been silently disabled since 2.3.0.
- The completion beep no longer waits a second after its last ring.

## [2.3.6] - 2026-10-14

### Fixed

- The logger created an empty log file on every run, even `typy version`.
  Log files are now created lazily, on the first message.

## [2.3.5] - 2026-10-09

### Fixed

- `pathspec` 1.0 deprecation warning: `.typyignore` now uses the `gitignore`
  pattern factory and only falls back to `gitwildmatch` on older installs.

## [2.3.4] - 2026-10-05

### Fixed

- A module docstring came out single-quoted in generated code.

## [2.3.3] - 2026-09-29

### Performance

- Project discovery prunes hidden, ignored and `__pycache__` folders while
  walking instead of listing everything and filtering afterwards.

## [2.3.2] - 2026-09-22

### Fixed

- `--standalone` archives lost their executable bit when copied into `output/`.

## [2.3.1] - 2026-09-17 (hotfix)

### Fixed

- `typy build --gui` without `--enforce` crashed while installing the monitor.
  It is now ignored with a note, since there is nothing to monitor.

## [2.3.0] - 2026-09-15

Enforcement grows up.

### Added

- **Return values are enforced** with `--enforce`: every `return` is checked
  against the declared type, and so is a function that runs off its end.
- **Augmented assignments are re-checked** (`int total = 1; total += 1.5` fails).
- Elements collected by `*type name` / `**type name` are checked one by one.
- `None` and `Ellipsis` typed variables are enforced (as `type(None)` and
  `type(Ellipsis)`).
- `match` capture names, `with ... as` and walrus targets count as declarations.
- The `docs/` folder: language reference, CLI, build system, AST, runtime,
  diagnostics, architecture, contributing and release process.

### Changed

- The runtime is now two packages shipped with a build: `_typy_runtime`
  (the checks) and `_typy_monitor` (only with `--gui`). The monitor starts by
  itself when the program first imports the runtime, so no file opts in.
- The code base was restructured so that no module defines more than two
  functions; package `__init__` files hold the public surface.
- `void` misuse checks resolve names through scopes, so a local variable
  that shadows a void function is no longer reported.

## [2.2.3] - 2026-08-04

### Fixed

- `typy import --override` could leave a half-replaced folder if verification
  failed; the archive is now verified completely before anything is touched.

## [2.2.2] - 2026-07-09

### Fixed

- `typy export` included `__pycache__` folders and older `.typyexp` archives.

## [2.2.1] - 2026-06-30

### Fixed

- `typy stats` crashed on a damaged `stats.json`; it now reads as empty.

So long, nerds. 🐷👑

## [2.2.0] - 2026-06-15

Sharing projects.

### Added

- `typy export <project>` packages a project as a `.typyexp` archive
  (zip + manifest with a SHA-256 per file) and `typy import <file>` unpacks
  one, verifying every file and refusing paths that escape the destination.
- `typy stats` shows what Typy has done on this machine (`--json`, `--reset`).
- `typy version [--modules]`, backed by a module registry.
- Typed variadic parameters: `*int values`, `**str options`.

### Changed

- **Language:** the compiler-owned throwaway name is now `__` (two
  underscores) and `repeat` lowers to `for __ in range(...)`. A single `_` is
  an ordinary identifier again, so `for _ in ...` and `x, _ = pair` work.
- `--gui` moved to `typy build`: the monitor now starts from the built
  program's entry point.

### Removed

- `typy check`, `typy run` and `typy clean`. Build to check, run the output
  with Python, rebuild with `--override` to clean.

## [2.1.3] - 2026-05-12

### Fixed

- Error columns were off by one on lines that start with a decorator.

## [2.1.2] - 2026-04-07

### Performance

- Statement classification no longer re-scans a line once per pattern.

## [2.1.1] - 2026-03-19 (hotfix)

### Fixed

- Chains nested inside subscript keys (`a[b?.c]`) were not rebuilt as
  optional chains after the move to the AST.

## [2.1.0] - 2026-03-15

The Typy AST.

### Added

- **The Typy AST is officially supported.** Typy now has its own syntax tree
  (`tree/`), built by a real parser (`parser/`) and lowered to Python by its
  own stage (`lowering/`). Typy nodes extend Python's `ast`, so every tool
  that walks Python trees walks Typy trees too.
- Positional-only (`/`) and keyword-only (`*`) markers in typed signatures.
- Every semantic error in a file is reported in one run, sorted by position,
  with typed error classes and hints.
- `formatting/`: signature printing, used by `--veritasium`.

### Changed

- Generated imports are inserted after the module docstring and any
  `from __future__` imports instead of always at the very top.

## [2.0.3] - 2025-12-15

### Performance

- The compiler caches the offset table per file instead of per
  statement; large files compile about three times faster.

- Yeah, this one's on me, I have no idea why I made it that way.

### Fixed

- `elunless` directly after `unless` lost its negation when the condition
  spanned several lines.

## [2.0.2] - 2025-10-21 (hotfix)

### Fixed

- Projects whose folder name contained a space failed to build after the
  switch to staged output.

## [2.0.1] - 2025-09-15

### Changed

- Builds are now all-or-nothing: everything is compiled first, assembled in a
  temporary staging folder and only then copied to `output/`.

- PS: Contributors, `bootstrap/_stage0.py` is not a mistake, it's a feature!

### Fixed

- The compiler mis-lowered nested `repeat` loops that shared a
  counter.

## [2.0.0] - 2025-08-01

### Changed

- **Typy is now self-hosted.** The compiler is compiled by itself; the
  stage-0 host that bootstrapped it is retired and `bootstrap/_stage0.py` is
  empty. Or is it?

## [1.5.2] - 2025-06-30

### Fixed

- The monitor printed its summary twice when the program called `sys.exit`.

So long, nerds. 🐷👑

## [1.5.1] - 2025-06-17 (hotfix)

### Fixed

- `--notify` blocked the terminal until the media player was closed.

## [1.5.0] - 2025-06-15

### Added

- `--notify`: a completion beep. There is also a 1 in 69 chance of something
  else. It falls back to the beep if that something else is unavailable.
- `--enforce --gui`: a live monitor of every runtime check, across every file
  of the program, through a hook in the runtime.
- `tools/`: every standard-library module the compiler uses is reached
  through one facade, the first piece of a Typy standard library.
- `bootstrap/`: the stage-0 host, groundwork for a self-hosted compiler.

## [1.4.2] - 2025-05-06

### Fixed

- `--bytecode` left the temporary `.py` next to the `.pyc` when compilation
  of that file failed.

## [1.4.1] - 2025-03-18 (hotfix)

### Fixed

- `--standalone` failed for projects whose entry point was `main.typy`
  rather than `__main__.typy`.

## [1.4.0] - 2025-03-15

### Added

- `--bytecode`: emit `.pyc` instead of `.py`.
- `--standalone`: pack a build into one runnable archive. Mutually exclusive
  with `--bytecode`.
- `--veritasium`: verbose, stage-by-stage compiler output.
- `logger/`: a crash and event log plus usage counters.

## [1.3.2] - 2025-02-04

### Fixed

- Negated `.typyignore` patterns (`!keep.log`) were ignored.

## [1.3.1] - 2025-01-09

### Fixed

- Resource files in nested folders were copied to the output root.

## [1.3.0] - 2024-12-15

### Added

- `.typyignore`, with `.gitignore` semantics.
- Project builds copy every non-Typy file (assets, data, plain `.py`) into
  `output/`; `--lightweight` copies only `.typy` and `.py` files.

## [1.2.7] - 2024-12-04

### Fixed

- `--override` deleted `output/` before checking that the build would succeed.

## [1.2.6] - 2024-11-26

### Fixed

- A `.py` file next to a `.typy` file of the same name silently replaced the
  compiled output; this is now an error.

## [1.2.5] - 2024-11-12

### Performance

- Reserved-word checks use frozen sets instead of lists.

## [1.2.4] - 2024-10-29

### Fixed

- Building a single file wrote its output next to the current directory
  instead of next to the file.

## [1.2.3] - 2024-10-14

### Fixed

- `__init__.py` files were generated in folders that held no Python.

## [1.2.2] - 2024-10-02

### Fixed

- Error locations showed 0-based columns.

## [1.2.1] - 2024-09-18 (hotfix)

### Fixed

- Hidden folders (`.git`, `.venv`) were compiled as part of the project.

## [1.2.0] - 2024-09-15

### Added

- Project builds: `typy build project/` compiles every `.typy` file into
  `project/output/`, mirroring the folder layout.
- `--override`: an existing `output/` is never replaced without it.
- `typy <target>` as shorthand for `typy build <target>`.
- Typed errors (`errors/`) with clean messages instead of tracebacks.

## [1.1.2] - 2024-07-29

### Fixed

- A trailing `?` (`user?.name?`) was silently ignored; it is now an error.

## [1.1.1] - 2024-06-30 (hotfix)

### Fixed

- Arguments of a call after a `None` link were still evaluated
  (`user?.save(expensive())`); the rest of a chain is now fully skipped.

So long, nerds. 🐷👑

## [1.1.0] - 2024-06-15

### Added

- Optional chaining: `a?.b`, `a?[k]`, `a?.method()`. A `None` before a
  guarded link turns the whole rest of the chain into `None`, lazily.

## [1.0.2] - 2024-04-11

### Fixed

- `--enforce` wrapped annotation-only declarations (`x: int`) in a check.

## [1.0.1] - 2024-03-21

### Fixed

- An `any` declared inside a loop kept the type from the previous iteration.

## [1.0.0] - 2024-03-15

Typy v1: the language specification is frozen.

### Added

- `--enforce`: optional runtime type enforcement, by exact type (a `bool` is
  not an `int`), with the runtime module shipped next to the output.
- The declare-before-assigning rule: `x = 10` needs an earlier `int x = ...`.

## [0.4.1] - 2024-01-08

### Fixed

- Initialized loops nested inside other initialized loops were not rewritten.

## [0.4.0] - 2023-12-15

### Added

- Initialized loops: `i(0) while i < 10:` and `i(0) until i >= 10:`, whose
  variables are deleted however the loop ends.
- `any` (type fixed by the first value) and `dyn` (never enforced).

## [0.3.2] - 2023-10-30

### Performance

- Statement keywords are detected in one pass over the token stream.

## [0.3.1] - 2023-09-19 (hotfix)

### Fixed

- `repeat` inside a function body was not recognised.

## [0.3.0] - 2023-09-15

### Added

- `until`, `forever`, `repeat`, `unless` and `elunless`.

## [0.2.1] - 2023-06-30

### Fixed

- `None` was rejected as a return type because Python treats it as a keyword.

So long, nerds. 🐷👑

## [0.2.0] - 2023-06-15

### Added

- Typed function signatures: `int add(int a, int b):`. Plain `def` is not Typy.
- `void` (no return at all) and `None` return types.
- Nested classes and qualified types (`Parent.Car car = Parent.Car()`).
- Compile-time literal mismatch detection (`int x = 10.5`).

## [0.1.2] - 2023-04-03

### Fixed

- Files with Windows line endings reported columns one too far right.

## [0.1.1] - 2023-03-22

### Fixed

- Tabs inside string literals were rejected as indentation.

## [0.1.0] - 2023-03-15

First release.

### Added

- Typed declarations: `int x = 10` compiles to `x: int = 10`.
- Reserved identifiers, the no-tabs rule and delimiter checking.
- `typy file.typy` compiles one file to Python.
