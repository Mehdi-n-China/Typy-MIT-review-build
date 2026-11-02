# Release process

## Versions

Typy follows semantic versioning, `MAJOR.MINOR.PATCH`:

- **MINOR** (`2.4.0`): something notable: a language feature, a command, a new
  stage. Minor releases only ship on the regular schedule.
- **PATCH** (`2.3.10`): a fix or a small optimization.
- **MAJOR** (`3.0.0`): a change of era, released when it is ready rather than
  on the schedule. 2.0.0, the self-hosting release, shipped on 2025-08-01.

## Schedule

Regular releases land on the **15th of March, June, September and December**.
A quarter with a feature ready gets a minor release; a quarter without one
still gets a patch release with whatever fixes are pending. Hotfixes ship
whenever they are needed and are marked `(hotfix)` in the changelog.

The next scheduled release is **2.4.0 on 2026-12-15**.

## Cutting a release

1. Move the `Unreleased` entries in `CHANGELOG.md` under a new heading:
   `## [X.Y.Z] - YYYY-MM-DD`, adding ` (hotfix)` when it is one.
2. Update `version` and `released` in `../source/__version__.typy`.
3. Give any new package a `Since: X.Y.Z` docstring line and a row in
   `../source/registry/_modules.typy`, then rebuild (`python -m typy.bootstrap`).
4. Run `python -m typy.bootstrap --check`: the release must be a fixpoint of
   its own sources.
5. Run the tests; `test_changelog.py` checks the schedule, the ordering, the
   version file and every `Since:` note against the changelog.
