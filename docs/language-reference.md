# Language reference

**Typy behaves exactly like Python except where this page says otherwise.**
Everything not mentioned here (expressions, operators, comprehensions,
generators, decorators, `with`, `match`, exceptions, imports, `async`, lambdas,
scoping) is Python, parsed by Python's own parser.

Each section shows Typy source and the Python it compiles to.

## Typed declarations

```typy
int x = 10
str name = "Alice"
Parent.Car car = Parent.Car()
```

```python
x: int = 10
name: str = 'Alice'
car: Parent.Car = Parent.Car()
```

The form is `TYPE name = value`. Types may be dotted to any depth and do not
have to exist for the line to parse (`Car x = Not_A_Car()` is fine). A
declaration always needs a value; `int x` on its own is an error.

### Declare before assigning

A plain assignment is only valid for a name the scope already knows:

```typy
int x = 10
x = 20        # fine: x was declared
y = 5         # error: 'y' is not declared
```

A name is known if anything in the same scope binds it: a typed declaration, a
parameter, a `for` / `with ... as` / `except ... as` target, an import, a
function or class definition, a walrus target, a `match` capture, a
`global` / `nonlocal` statement. Like Python's own local-variable rule, the
whole scope is considered, not just the lines above. Unpacking targets are
checked name by name.

Redeclaring changes the type information from that point on:

```typy
int x = 10
str x = "hello"   # x is a str now
```

Python-style annotations (`x: int`, `x: int = 5`) also work and count as
declarations.

## Functions

Functions are declared with a typed signature. Python's `def` is not valid Typy.

```typy
int add(int a, int b = 5):
    return a + b

void log(str message):
    print(message)

async str fetch(str url):
    ...
```

```python
def add(a: int, b: int=5) -> int:
    return a + b

def log(message: str) -> None:
    print(message)

async def fetch(url: str) -> str:
    ...
```

Every parameter has a type and every function has a return type. Parameters
support everything Python's do:

| Typy | Python | Meaning |
| --- | --- | --- |
| `int a` | `a: int` | positional-or-keyword |
| `int a = 1` | `a: int = 1` | with a default |
| `/` | `/` | everything before is positional-only |
| `*` | `*` | everything after is keyword-only |
| `*int values` | `*values: int` | extra positional arguments, each an `int` |
| `**str options` | `**options: str` | extra keyword arguments, each a `str` |

Methods are ordinary typed functions inside a class; `self` needs a type too,
usually `dyn self`:

```typy
class Counter:
    None __init__(dyn self, int start = 0):
        self.value = start
```

### `void` and `None`

`void` means the function produces no value at all. It may not contain any
`return` (not even a bare one), and calling it is only allowed as a statement
on its own: `x = f()`, `print(f())`, `return f()` are all errors.

`None` is an ordinary return type: `return` and `return None` are both fine.

Both compile to `-> None`; the difference only exists at compile time.

## Conditionals

```typy
unless ready:
    wait()
elunless retries > 3:
    retry()
elif fatal:
    give_up()
else:
    proceed()
```

```python
if not ready:
    wait()
elif not retries > 3:
    retry()
elif fatal:
    give_up()
else:
    proceed()
```

`unless` is `if not (...)` and `elunless` is `elif not (...)`. Both openers
(`if`, `unless`) and both continuations (`elif`, `elunless`) mix freely.

## Loops

| Typy | Python |
| --- | --- |
| `until done:` | `while not done:` |
| `forever:` | `while True:` |
| `repeat n:` | `for __ in range(n):` |

All three accept an `else:` block with Python's loop-`else` meaning.

`repeat` has no visible loop variable. It uses `__` (two underscores), which is
reserved, so user code can neither collide with it nor read it.

### Initialized loops

```typy
i(0), j(10) while i < j:
    i += 1
    j -= 1
```

```python
i: Any = 0
j: Any = 10
try:
    while i < j:
        i += 1
        j -= 1
finally:
    del i, j
```

The variables exist only for the loop: they are created before the first test
and deleted however the loop ends (normally, `break`, or an exception). They
are `dyn`, never enforced, and nothing is incremented for you. `until` works
the same way: `i(0) until i >= 10:`. These are throwaway variables; an existing
variable of the same name is replaced and then deleted.

## Optional chaining

```typy
dyn city = user?.address?.city
dyn first = rows?[0]
dyn upper = name?.upper()
```

A `?` in front of `.` or `[` guards that step: if the value it would act on is
`None`, the **whole rest of the chain** evaluates to `None`, and nothing after
that point runs (later attributes, call arguments, subscript keys). Steps
written without `?` are ordinary Python and raise as usual.

```python
city: Any = None if (_typy_ch1 := user) is None else None if (_typy_ch2 := _typy_ch1.address) is None else _typy_ch2.city
```

Rules: the `?` must be glued to the following `.` or `[`; a trailing `?` and
`?(` are errors; a chain cannot be assigned to or deleted. Missing attributes
are *not* silenced: only `None` is special.

## Reserved words

These can never be *defined* (as a variable, parameter, function, class, loop
target, import alias...):

```text
__  any  dyn  void  repeat  unless  elunless  forever  until  typy
```

Referencing them is fine, which is why Python's builtin `any(...)` still works.
A single `_` and names merely starting with underscores (`_temp`,
`__internal`) are ordinary identifiers.

## Indentation and delimiters

Blocks are indented as in Python. Tabs are not allowed for indentation (tabs
elsewhere, inside strings for example, are fine). Unclosed or mismatched
brackets are reported with the delimiter that is missing.

## Not part of the language

`const`, typed `for` loops, expression-bodied functions, `|>`, `??`, and
replacements for `elif`, comprehensions, generators, `match` or `with` are
deliberately absent: Python already expresses them.
