"""Parsing compound-statement headers with a dummy body."""
from typing import Any
from ._guards import segment_text
from ._parse_text import parse_python_text
from ._context import ParseContext

def parse_header(ctx: ParseContext, tokens: list, prefix: str='', suffix: str=' pass', col_shift: int=0) -> Any:
    """Parse a header such as ``for x in y:`` by giving it a dummy body.

    ``tokens`` are the header tokens up to and including the colon. The stub
    ``for x in y: pass`` is handed to Python and the first statement of the
    result returned; the caller swaps in the real, Typy-parsed body. A
    ``prefix`` supplies surrounding context some headers need (``except``
    must sit inside a ``try``), ``suffix`` replaces the dummy body and
    ``col_shift`` corrects columns when the prefix indented the header.
    """
    text: str = prefix + segment_text(ctx, tokens) + suffix
    stub_line: Any = prefix.count('\n') + 1
    return parse_python_text(ctx, text, 'exec', tokens[0], stub_line=stub_line, col_shift=col_shift).body[0]
