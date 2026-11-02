"""Stamping source locations onto nodes."""
from typing import Any
from .. import tools

def place(node: Any, first: tools.tokens.TokenInfo, last: Any=None) -> Any:
    """Give ``node`` the location spanning tokens ``first`` .. ``last``.

    ``last`` defaults to ``first``. Returns ``node`` so calls can be chained.
    Locations use Python's conventions: 1-based lines, 0-based columns.
    """
    last = last or first
    node.lineno = first.start[0]
    node.col_offset = first.start[1]
    node.end_lineno = last.end[0]
    node.end_col_offset = last.end[1]
    return node
