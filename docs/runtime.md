# Runtime

Code built with `--enforce` imports a small support package:

```python
import _typy_runtime as typy
```

It is copied into every such build as `output/_typy_runtime/`, never imports
the compiler, and works with no Typy installed. Its source is
`typy/runtime/typy/`.

## API

| Function                              | Used for                                                                 |
| ------------------------------------- | ------------------------------------------------------------------------ |
| `typy.check(value, type, name)`       | A declared name, a parameter, a return value. Returns `value` or raises. |
| `typy.check_any(value, state, name)`  | An `any` binding: the first call fixes the type, later calls enforce it. |
| `typy.AnyState()`                     | The memory of one `any` declaration.                                     |
| `typy.check_each(values, type, name)` | Every element of a `*` / `**` parameter.                                 |
| `typy.TypyTypeError`                  | Raised on a failed check (a subclass of `TypeError`).                    |
| `typy.set_monitor(callback)`          | Observe every check (used by the monitor).                               |

Every check compares `type(value) is expected`: exact types only.

Typical generated code:

```python
x: int = typy.check(10, int, 'x')

def square(n: int) -> int:
    n = typy.check(n, int, 'n')
    return typy.check(n * n, int, 'square() return')
```

A failure reads `x: expected int, got str`, or for `any`,
`x: established as int, got str`.

## The enforcement monitor (`--gui`)

Build with `typy build --enforce --gui` and the build also ships
`output/_typy_monitor/` and switches the runtime copy's `_config.GUI` on. The
first time the program imports the runtime (which every compiled file does
before anything else), the monitor attaches itself to the runtime's hook. From
then on it sees every check made anywhere in the program, in every file, with
no file opting in:

```text
=== Typy enforcement monitor -- entry point: output ===
  ok    n                      kind=concrete expected=int          got=int
  ok    square() return        kind=concrete expected=int          got=int
  FAIL  name                   kind=any      expected=int          got=str
=== enforcement summary ===
  checks performed : 3
  passed           : 2
  failed           : 1
  elapsed          : 0.0004s
  names with failures:
    name: 1 of 1 check(s) failed
```

The monitor prints to stderr and its summary appears when the program exits,
even if it exits through an uncaught error. It only observes: it never
recomputes or changes a check, and an error inside the monitor is swallowed
rather than allowed to affect the program. The interface is text-mode; a
graphical front-end can attach to the same hook (`typy.set_monitor`).
