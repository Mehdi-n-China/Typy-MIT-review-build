"""Python's ``for`` / ``async for`` loops."""
from typing import Any
from ._header_stub import parse_header
from ._body import parse_body, require_header_colon
from ._else_clause import parse_else_clause
from ..lexer import LogicalLine
from ._context import ParseContext

def parse_for(ctx: ParseContext, lines: list, index: int, decorators: list) -> tuple:
    """Parse a ``for`` header with Python's parser, then swap in the
    Typy-parsed body and optional ``else``."""
    line: LogicalLine = lines[index]
    colon: int = require_header_colon(ctx, line, 'for')
    node: Any = parse_header(ctx, line.tokens[:colon + 1])
    node.body = parse_body(ctx, line, colon, "'for'")
    node.orelse, index = parse_else_clause(ctx, lines, index + 1)
    return ([node], index)
