# Type system

Typy's typing has two halves: **compile-time checks** that only cover what the
compiler can know for certain, and **runtime enforcement** (`--enforce`) that
checks everything else while the program runs.

## Compile time

The compiler checks:

- reserved words are never defined;
- every assigned name was declared;
- a **literal** value matches its declared type;
- `void` functions never `return` and their results are never used.

### Literals

Only values that are *directly* a literal are compared with their declared
type:

| Category | Recognised literals |
| --- | --- |
| `int`, `float`, `complex` | `1`, `-5`, `1.5`, `3+4j` |
| `str`, `bytes` | `"a"`, `b"a"` |
| `bool` | `True`, `False` |
| `None` | `None` |
| `list`, `tuple`, `set`, `dict` | `[...]`, `(...)`, `{1}`, `{}` |
| `Ellipsis` | `...` |

```typy
int a = 10.5          # error: declared int, value is a float literal
float b = 1           # error: exact types, an int literal is not a float
int c = some_call()   # fine: arbitrary expressions are trusted
int d = 1 + 2         # fine: an expression, not a literal
```

The same check applies to parameter defaults (`int f(int x = 1.5)`).

Typy never tries to work out what an arbitrary expression returns. That is a
design decision, not a gap: anything the compiler cannot know is left to
`--enforce`.

## Runtime enforcement

Build with `--enforce` and the generated program checks its own types:

| What | Check |
| --- | --- |
| `int x = v` and later `x = v` | `v` must be exactly an `int` |
| `x += v` | `x` is re-checked afterwards |
| parameters | checked when the function starts |
| `*int values`, `**str opts` | every element is checked |
| `return v` | `v` must match the return type |
| running off the end | the implicit `None` must match the return type |

Without `--enforce` nothing is inserted and there is no runtime cost.

### Exact types

Matching is `type(value) is expected`. A `bool` is not an `int`, a subclass does
not satisfy its parent, and an `int` is not a `float`.

### `any`, `dyn`, `void`, `None`

| Type | Meaning |
| --- | --- |
| `any` | The first value fixes the type; later assignments must match it exactly. |
| `dyn` | Anything, any time. Never enforced. |
| `void` | Return type only: the function produces no value. |
| `None` | A real type: the value `None`. |

```typy
any count = 5
count = 6        # fine: established as int
count = "six"    # runtime error with --enforce
```

An `any` declaration with a literal value is fully known at compile time; with a
non-literal value its type is established when the program runs. Each `any`
declaration remembers its type separately, and re-running the declaration
(say, inside a loop) starts over.

`any` and `dyn` both appear as `typing.Any` in generated annotations.

## What enforcement does not cover

- Assignments to attributes and subscripts (`obj.x = ...`, `items[0] = ...`).
- Names assigned through `global` / `nonlocal`, walrus expressions, or `for`
  targets that reuse a declared name.
- Return values of generator functions.
- Complex annotations such as `list[int]`, which Typy cannot name; Python-style
  annotations of that kind are left to Python.
- Anything across files at compile time: each file is compiled on its own, so
  calling an imported `void` function as a value is only caught if you check
  it yourself.
