# The Typy AST

The Typy AST is Python's `ast` plus the node classes below (all in `tree/`).
Ordinary Python constructs stay ordinary `ast` nodes. Every Typy node carries
the usual `lineno` / `col_offset` / `end_lineno` / `end_col_offset`.

## Statements

| Node                  | Fields                                                | Source                 | Lowers to                                       |
| --------------------- | ----------------------------------------------------- | ---------------------- | ----------------------------------------------- |
| `TypedDeclaration`    | `type`, `name`, `value`                               | `int x = 1`            | `x: int = 1`                                    |
| `FunctionDeclaration` | `name`, `signature`, `body`, `decorators`, `is_async` | `int f(int a):`        | `def f(a: int) -> int:`                         |
| `Conditional`         | `branches`, `orelse`                                  | `if` / `unless` chains | nested `if` / `elif` / `else`                   |
| `UntilLoop`           | `test`, `body`, `orelse`                              | `until c:`             | `while not c:`                                  |
| `ForeverLoop`         | `body`, `orelse`                                      | `forever:`             | `while True:`                                   |
| `RepeatLoop`          | `count`, `body`, `orelse`                             | `repeat n:`            | `for __ in range(n):`                           |
| `InitializedLoop`     | `bindings`, `mode`, `test`, `body`, `orelse`          | `i(0) while c:`        | declarations + `try` / `while` / `finally: del` |

## Expressions

| Node            | Fields          | Source       |
| --------------- | --------------- | ------------ |
| `OptionalChain` | `base`, `links` | `a?.b[c](d)` |

Lowers to nested `None if (t := x) is None else ...` expressions; see the
[language reference](language-reference.md).

## Auxiliary nodes

| Node          | Fields                                                 | Notes                                                                                                                               |
| ------------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| `TypeRef`     | `parts`                                                | A dotted type name. `text`, `is_any`, `is_dyn`, `is_void`, `is_none`, `to_expression()`.                                            |
| `Signature`   | `parameters`, `returns`                                | `returns` is a `TypeRef`.                                                                                                           |
| `Parameter`   | `name`, `type`, `default`, `kind`                      | `kind`: `normal`, `slash`, `star`, `vararg`, `kwarg` (`ParameterKind`). `formatted` renders it; `a + b` builds a `ParameterVector`. |
| `Branch`      | `kind`, `test`, `body`                                 | `kind` is `if`, `unless`, `elif` or `elunless`; `negated` is true for `unless` and `elunless`.                                      |
| `LoopBinding` | `name`, `value`                                        | One `i(0)` of an initialized loop.                                                                                                  |
| `ChainLink`   | `kind`, `guarded`, `name`, `index`, `args`, `keywords` | One step of a chain: `attr`, `sub` or `call`.                                                                                       |
| `Program`     | `body`, `filename`                                     | The root.                                                                                                                           |

## Helpers

- `place(node, first_token, last_token)` stamps a location.
- `child_blocks(node)` yields every statement list nested in a compound
  statement (bodies, `orelse`, clause bodies), Python and Typy alike.
- `map_blocks(node, function)` rewrites those blocks in place.
- `is_scope_node(node)` is true for functions and classes.

## Example

```python
>>> from Typy.parser import parse_source
>>> import ast
>>> program, _ = parse_source("unless ready:\n    go()\n")
>>> print(ast.dump(program.body[0]))
Conditional(branches=[Branch(kind='unless', test=Name(id='ready', ctx=Load()),
body=[Expr(value=Call(func=Name(id='go', ctx=Load()), args=[], keywords=[]))])], orelse=[])
```
