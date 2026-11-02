# Getting started

## Requirements

- Python 3.14 or newer. Might work for lower versions but not supported.
- [`pathspec`](https://pypi.org/project/pathspec/) for `.typyignore` matching:
  `pip install -r typy/requirements.txt`.

Typy needs no installation step. The `Typy` folder _is_ the package; run it
from the folder that contains it:

```text
parent/
└── typy/          <- this repository
```

```bash
cd parent
python -m typy version
```

## A first program

`hello.typy`:

```typy
str greet(str who):
    return "hello " + who

int count = 3
repeat count:
    print(greet("typy"))
```

```bash
python -m typy build hello.typy          # or simply: python -m typy hello.typy
python output/hello.py
```

The build writes `output/hello.py` next to the source file:

```python
def greet(who: str) -> str:
    return 'hello ' + who

count: int = 3
for __ in range(count):
    print(greet('typy'))
```

Add `--enforce` and the program checks its own types while it runs:

```bash
python -m typy build hello.typy --enforce --override
```

## A first project

A project is a folder. Every `.typy` file in it is compiled, every other file is
copied along (unless `.typyignore` excludes it), and the result lands in
`project/output/` with the same layout. Name the entry point `__main__.typy` and
the output folder runs directly:

```bash
python -m typy build my_project --enforce
python my_project/output
```

`typy/example_project` is a small project that uses most of the language.

## Next steps

- What the language adds: [language reference](language-reference.md).
- Every flag: [command line](cli.md).
- Why your build failed: [diagnostics](diagnostics.md).
