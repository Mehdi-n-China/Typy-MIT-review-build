# Architecture

## The pipeline

```text
source text
  │  lexer         tokens -> logical lines nested by indentation
  ▼
logical lines
  │  parser        Typy statements -> Typy nodes, everything else -> Python's parser
  ▼
Typy AST           (Python's ast, extended with Typy node classes)
  │  semantics     reserved words, declarations, literals, void rules
  ▼
annotated AST
  │  enforcement   runtime checks inserted              [--enforce only]
  ▼
  │  lowering      every Typy node replaced by plain Python nodes
  ▼
Python AST
  │  codegen       imports added, ast.unparse
  ▼
Python source
```

`pipeline.compile_to_python` wires the stages together; `compiler.compile_source`
wraps it so errors come back as data instead of exceptions.

## Key ideas

**Only parse what Typy adds.** The parser recognises Typy's statement forms
itself and cuts every other statement or expression out of the source as exact
text, handing it to Python's own `ast.parse`. Python's grammar is therefore
Python's by construction; Typy never re-implements it.

**Extend Python's AST, don't replace it.** Typy nodes subclass `ast.stmt` /
`ast.expr`, so a mixed tree works with `ast.walk`, `ast.dump` and visitors,
and a Typy node can appear anywhere a Python node of the same kind can (an
`OptionalChain` inside a call argument, a `TypedDeclaration` inside a `with`).

**Optional chaining through a marker.** Before Python parses a snippet, every
`?` is replaced by an attribute access on a name users cannot write
(`a?.b` -> `a .__typyg__.b`). After parsing, the marker is found and the chain
rebuilt as an `OptionalChain` node. Positions survive, and Python still
validates the surrounding expression.

**Stages are small and separate.** Each stage is its own package, and each
pass inside it is its own module. Lowering is table-driven: one handler per
Typy node class, registered in `lowering/__init__.py`.

## Self-hosting

Typy is written in Typy. `../source/` holds the compiler as `.typy` files,
mirroring the package, and every `.py` file of the package is the compiled
form of one of them:

```text
source/semantics/_scope.typy   --compiled by Typy-->   semantics/_scope.py
```

`python -m Typy.bootstrap` compiles every source with the compiler that is
currently installed and writes the results into the package;
`python -m Typy.bootstrap --check` writes nothing and fails if any module
would change. A healthy checkout is a **fixpoint**: compiling the sources
with the compiler they describe reproduces that compiler byte for byte. The
test-suite checks this on every run.

Changing the compiler therefore takes up to three rebuilds. The first is the
old compiler compiling the new sources. The second is the new compiler
compiling them again, which matters when the change affects generated code.
The third must report no changes.

The generated `.py` files carry the sources' docstrings but not their
comments (Python's `ast` does not keep comments); the sources are where
the code is read and edited. Two files are hand-written on purpose:
`bootstrap/_stage0.py`, the remains of the stage-0 host that compiled the very
first Typy-written compiler, and the test-suite, which stays plain Python so
it can test a broken compiler.

## Package map

| Package | Role |
| --- | --- |
| `lexer` | Normalisation, tokenizing, logical lines, the no-tabs rule, token helpers |
| `parser` | Statement parsers, the bridge to Python's parser, optional-chain rebuilding |
| `tree` | The Typy AST node classes and generic block helpers |
| `semantics` | Scopes, bindings, every compile-time check |
| `enforcement` | Runtime-check injection |
| `lowering` | Typy AST -> Python AST |
| `codegen` | Imports and printing |
| `context` | `CompileContext`: per-compilation state and generated names |
| `formatting` | Signature printing |
| `runtime` | Code shipped with compiled programs (never imports the compiler) |
| `builder` | Planning, staging and publishing builds |
| `packaging` | `--bytecode` and `--standalone` |
| `ignore` | `.typyignore` |
| `archive` | `.typyexp` export/import |
| `notifications` | `--notify` |
| `errors` | Error classes |
| `logger` | Event log and usage counters |
| `registry` | The module table of `typy version --modules` |
| `tools` | Facade over the standard library |
| `cli` | Commands and argument parsing |
| `bootstrap` | Rebuilds the package from `../source/` with itself (`python -m Typy.bootstrap`) |

## Data flow between stages

The semantic stage annotates the tree for later stages instead of returning a
separate symbol table:

| Attribute | Set on | Meaning |
| --- | --- | --- |
| `binding` | declarations, assignments, parameters | how the target name is bound (`concrete`, `any`, `dyn`, `exempt`) |
| `scope` | `Program`, functions, classes | the `Scope` they open |

`CompileContext` carries what every stage shares: the enforce flag, the set of
names already used in the file (generated names avoid them), and the flags
that decide which imports the output needs.
