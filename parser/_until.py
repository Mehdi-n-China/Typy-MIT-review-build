"""``until condition:`` (spec §19)."""
from typing import Any
from ..tree import UntilLoop, place
from ._bridge import parse_python_expression
from ._body import parse_body, require_header_colon
from ._else_clause import parse_else_clause
from ._errors import syntax_error
from ..lexer import LogicalLine
from ._context import ParseContext

def parse_until(ctx: ParseContext, lines: list, index: int, decorators: list) -> tuple:
    """Parse ``until test:`` (with an optional ``else:``)."""
    line: LogicalLine = lines[index]
    colon: int = require_header_colon(ctx, line, 'until')
    if colon == 1:
        raise syntax_error(ctx, "'until' needs a condition", line.first)
    test: Any = parse_python_expression(ctx, line.tokens[1:colon])
    body: list = parse_body(ctx, line, colon, "'until'")
    orelse: Any = None
    orelse, index = parse_else_clause(ctx, lines, index + 1)
    return ([place(UntilLoop(test, body, orelse), line.first, line.tokens[colon])], index)
