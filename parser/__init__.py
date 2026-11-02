"""
Typy parser: logical lines -> Typy AST.

The parser only *understands* what Typy adds to Python: typed declarations,
typed function signatures, the new loop and conditional keywords, and the
optional-chaining operators. Everything else is cut out of the source as
exact text and handed to Python's own parser, so the rest of the language is
Python's by construction.

    _block / _classify / _dispatch    walk lines, decide what each one is
    _conditional ... _try _match      one module per statement form
    _bridge / _parse_text             the seam to Python's ``ast.parse``
    _guards / _chains                 optional chaining (``?.`` / ``?[``)
    _function / _parameters           typed signatures

Since: 2.1.0 (from 0.1.0 to 2.0.3 the compiler rewrote token streams instead).
"""
from ._parse_source import parse_source
