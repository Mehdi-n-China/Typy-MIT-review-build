"""Python's ``while`` loop."""
from typing import Any
from .. import tools
from ..tree import place
from ._bridge import parse_python_expression
from ._body import parse_body, require_header_colon
from ._else_clause import parse_else_clause
from ._errors import syntax_error
from ..lexer import LogicalLine
from ._context import ParseContext

def parse_while(ctx: ParseContext, lines: list, index: int, decorators: list) -> tuple:
    """Parse ``while test:`` (with an optional ``else:``)."""
    line: LogicalLine = lines[index]
    colon: int = require_header_colon(ctx, line, 'while')
    if colon == 1:
        raise syntax_error(ctx, "'while' needs a condition", line.first)
    test: Any = parse_python_expression(ctx, line.tokens[1:colon])
    body: list = parse_body(ctx, line, colon, "'while'")
    orelse: Any = None
    orelse, index = parse_else_clause(ctx, lines, index + 1)
    node: tools.pyast.While = tools.pyast.While(test=test, body=body, orelse=orelse)
    return ([place(node, line.first, line.tokens[colon])], index)
