"""Translating Python's own syntax errors into Typy diagnostics."""
from typing import Any
from .. import tools
from ..errors import TypyIndentationError, TypySyntaxError
from ._context import ParseContext

def convert_python_error(ctx: ParseContext, error: Any, first: tools.tokens.TokenInfo, stub_line: int=1, col_shift: int=0) -> Any:
    """Turn a ``SyntaxError`` raised while parsing a snippet into a
    ``TypySyntaxError`` (or ``TypyIndentationError``) located in the real file.

    ``first`` is the first token of the snippet; ``stub_line`` / ``col_shift``
    describe how the snippet was wrapped, mirroring ``relocate``.
    """
    snippet_line: Any = error.lineno or stub_line
    line: Any = first.start[0] + snippet_line - stub_line
    col: Any = None
    if error.offset:
        col = error.offset - 1
        if snippet_line == stub_line:
            col += first.start[1] + col_shift
    cls: Any = TypyIndentationError if isinstance(error, IndentationError) else TypySyntaxError
    return cls(error.msg, line, col, ctx.filename)
