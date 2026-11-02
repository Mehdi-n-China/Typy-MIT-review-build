# Command line

Run Typy from the folder that contains the `typy` package:

```bash
python -m typy <command> [options]
```

Examples below write `typy` for `python -m typy`.

## `typy build <target>`

Compile a `.typy` file or a project folder.

| Flag | Effect |
| --- | --- |
| `--enforce` | Insert runtime type checks ([type system](type-system.md)). |
| `--gui` | Ship the enforcement monitor; it starts with the program. Needs `--enforce` (ignored with a note otherwise). |
| `--override` | Replace an existing `output/`. Without it, an existing `output/` is never touched. |
| `--bytecode` | Write `.pyc` files instead of `.py`. |
| `--standalone` | Pack the build into one runnable `.pyz` archive. |
| `--lightweight` | Copy only `.typy`-derived and `.py` files, no other project files. |
| `--veritasium` | Verbose output: every stage of every file. |
| `--notify` | Beep when done. Occasionally something else. |

`--bytecode` and `--standalone` cannot be combined: both choose the output
format. Every other combination is allowed.

`typy <target> [flags]` (no command) is short for `typy build <target> [flags]`.

See [build system](build-system.md) for what ends up in `output/`.

## `typy export <project>`

Package a project folder as a `.typyexp` archive.

| Option | Effect |
| --- | --- |
| `-o FILE`, `--output FILE` | Where to write it (default: `<project>.typyexp` next to the project). |
| `--override` | Replace an existing archive. |

Exported: every file except `output/`, tool folders (`.git`, `__pycache__`,
`.venv`, `.idea`...), `.pyc` files, other archives and anything `.typyignore`
excludes. `.typyignore` itself is included. Format: [archive format](archive-format.md).

## `typy import <file.typyexp>`

Unpack an archive into a project folder.

| Option | Effect |
| --- | --- |
| `-o DIR`, `--output DIR` | Folder to create (default: the archive's name, next to it). |
| `--override` | Replace an existing folder **entirely**. |

The whole archive is extracted and verified in a temporary folder first:
every file's size and SHA-256 must match the manifest, no file may be missing
or unlisted, and no path may escape the destination. Only then is the
destination created or replaced.

## `typy stats`

Show the usage counters Typy keeps on this machine (builds, files compiled,
flags used, exports...). `--json` prints them raw; `--reset` zeroes them. The
data lives in `typy/stats/` (override with the `TYPY_STATS_DIR` environment
variable).

## `typy version`

Print the Typy version, its release date and the Python running it.
`--modules` adds every Typy module with the release that introduced it, and the
installed version of each dependency.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Success |
| 1 | A Typy error (compile errors, existing output, bad target...) |
| 2 | Invalid command line (from the argument parser) |
| 130 | Interrupted with Ctrl+C |

Errors are printed to stderr as `error: <file>:line-N:col-M: <message>`, often
followed by a `hint:` line. See [diagnostics](diagnostics.md).
