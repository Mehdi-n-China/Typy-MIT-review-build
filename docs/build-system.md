# Build system

## Targets

| Target | Root | Output |
| --- | --- | --- |
| `program.typy` | the file's folder | `<folder>/output/program.py` |
| `project/` | `project/` | `project/output/` mirroring the project |

## What a project build includes

Every `.typy` file under the project is compiled. Every other file is copied
to the same relative place, so data files, images and plain `.py` modules come
along. Left out:

- the top-level `output/` folder itself;
- hidden files and folders (name starts with `.`), `__pycache__`, `.pyc` files;
- `.typyignore` and everything it excludes.

`--lightweight` additionally drops every file that is not `.typy` or `.py`.

Folders that end up holding Python get an empty `__init__.py`, so the output
imports as a package tree (not in `--bytecode` builds, where folders import as
namespace packages).

A `.py` file whose path equals a compiled file's output (`util.typy` next to
`util.py`) is an error rather than a silent overwrite.

### `.typyignore`

Put a `.typyignore` in the project root. It uses `.gitignore` syntax: globs,
`**`, directory patterns (`build/`), anchoring (`/secret.txt`) and negation
(`!keep.log`).

```gitignore
*.log
scratch/
!important.log
```

## How a build runs

1. **Plan**: find the files.
2. **Check**: refuse early if `output/` exists and `--override` was not given.
3. **Compile everything.** Every file is compiled even after a failure, so all
   errors are reported together. Any error stops the build here, before the
   disk is touched.
4. **Stage** the output in a temporary folder: compiled files, copied files,
   package markers, the runtime.
5. **Publish**: replace `output/` with the staged folder.

A failed build therefore never leaves a half-written `output/` behind.

## The runtime

If any compiled file performs runtime checks (`--enforce`), the build ships
the runtime as `output/_typy_runtime/`. Generated code imports it as
`import _typy_runtime as typy`. Run the program from its output folder (or
with that folder on `PYTHONPATH`) so the import resolves; `python output/` and
`python output/main.py` both do.

With `--enforce --gui` the build also ships `output/_typy_monitor/` and turns
on a switch in the runtime copy, so the monitor starts as soon as the program
imports the runtime. See [runtime](runtime.md).

## Entry points

A project's entry point is `__main__.typy` (preferred) or `main.typy` at its
root. With `__main__.typy`, `python project/output` runs the program. The build
prints the command that runs what it built.

## `--bytecode`

Each compiled file is written as a `.pyc` (via `py_compile`) instead of a
`.py`. The runtime stays as source. Run the result with
`python output/main.pyc`.

## `--standalone`

The build is packed into a single `output/<name>.pyz` archive (`zipapp`) with a
shebang and the executable bit set: `./output/name.pyz` on Unix, or
`python output\name.pyz` anywhere. It needs an entry point.

Limitations, both inherent to zip applications:

- A Python interpreter is still required to run it; nothing is embedded.
- Files inside the archive cannot be opened by path. Read bundled data with
  `importlib.resources` or `pkgutil.get_data` instead of `open(__file__...)`.

## `--notify`

When the build finishes, the terminal bell rings three times. One build in 69
opens `assets/rickroll.mp4` with the system's media player instead; if the file
is missing or no player can be launched, it falls back to the bell.
