"""Bodies of compound statements, and the colon that introduces them."""
from typing import Any
from ..lexer import find_header_colon, LogicalLine
from ..reserved import STATEMENT_KEYWORDS
from ._errors import indentation_error, syntax_error
from ._segments import parse_segments
from ._context import ParseContext

def require_header_colon(ctx: ParseContext, line: LogicalLine, keyword: str, start: int=1) -> int:
    """Index of the colon ending ``line``'s header, or a clear error.

    A Typy keyword with no colon is almost always someone using the word as a
    variable name, so that case gets its own message.
    """
    colon: Any = find_header_colon(line.tokens, start)
    if colon is None:
        if keyword in STATEMENT_KEYWORDS:
            raise syntax_error(ctx, f'\'{keyword}\' is a reserved Typy keyword and cannot be used as an identifier', line.first, hint=f'as a statement it must look like \'{keyword} ...:\'')
        raise syntax_error(ctx, f'expected \':\' at the end of the \'{keyword}\' header', line.last)
    return colon

def parse_body(ctx: ParseContext, line: LogicalLine, colon: int, what: str) -> list:
    """Statements making up the body of the compound statement whose header
    ends at ``line.tokens[colon]``.

    The body is either the indented block under the line or, for the
    one-line form (``if x: y = 1``), whatever follows the colon.
    """
    from ._block import parse_block
    inline: list = line.tokens[colon + 1:]
    if inline:
        if line.children:
            raise indentation_error(ctx, 'unexpected indent', line.children[0].first)
        return parse_segments(ctx, inline)
    if not line.children:
        raise indentation_error(ctx, f'expected an indented block after {what}', line.tokens[colon])
    return parse_block(ctx, line.children)
