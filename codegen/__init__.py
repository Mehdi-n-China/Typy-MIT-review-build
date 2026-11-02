"""
Code generation: lowered Python AST -> source text.

Adds the imports generated code needs (after the docstring and any
``__future__`` imports) and prints the tree with ``ast.unparse``, except
f-strings, which get their own printer so the output runs on Python 3.14+
even when the compiler itself runs on 3.12+ (whose ``ast.unparse`` writes
f-strings older versions cannot read).

Since: 0.1.0 (moved to the AST printer in 2.1.0).
"""
from ._generate import generate_python
