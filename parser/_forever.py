"""``forever:`` (spec §20)."""
from typing import Any
from ..tree import ForeverLoop, place
from ._body import parse_body, require_header_colon
from ._else_clause import parse_else_clause
from ._errors import syntax_error
from ..lexer import LogicalLine
from ._context import ParseContext

def parse_forever(ctx: ParseContext, lines: list, index: int, decorators: list) -> tuple:
    """Parse ``forever:``; it takes no condition."""
    line: LogicalLine = lines[index]
    colon: int = require_header_colon(ctx, line, 'forever')
    if colon != 1:
        raise syntax_error(ctx, "'forever' does not take a condition", line.tokens[1], hint="use 'until' for a conditional loop")
    body: list = parse_body(ctx, line, colon, "'forever'")
    orelse: Any = None
    orelse, index = parse_else_clause(ctx, lines, index + 1)
    return ([place(ForeverLoop(body, orelse), line.first, line.tokens[colon])], index)
