"""``repeat N:`` (spec §21)."""
from typing import Any
from ..tree import RepeatLoop, place
from ._bridge import parse_python_expression
from ._body import parse_body, require_header_colon
from ._else_clause import parse_else_clause
from ._errors import syntax_error
from ..lexer import LogicalLine
from ._context import ParseContext

def parse_repeat(ctx: ParseContext, lines: list, index: int, decorators: list) -> tuple:
    """Parse ``repeat count:``."""
    line: LogicalLine = lines[index]
    colon: int = require_header_colon(ctx, line, 'repeat')
    if colon == 1:
        raise syntax_error(ctx, "'repeat' needs a number of times", line.first)
    count: Any = parse_python_expression(ctx, line.tokens[1:colon])
    body: list = parse_body(ctx, line, colon, "'repeat'")
    orelse: Any = None
    orelse, index = parse_else_clause(ctx, lines, index + 1)
    return ([place(RepeatLoop(count, body, orelse), line.first, line.tokens[colon])], index)
