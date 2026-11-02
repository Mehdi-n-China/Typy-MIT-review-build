"""Python's ``with`` / ``async with`` statements."""
from typing import Any
from ._header_stub import parse_header
from ._body import parse_body, require_header_colon
from ..lexer import LogicalLine
from ._context import ParseContext

def parse_with(ctx: ParseContext, lines: list, index: int, decorators: list) -> tuple:
    """Parse a ``with`` header with Python's parser and attach the body."""
    line: LogicalLine = lines[index]
    colon: int = require_header_colon(ctx, line, 'with')
    node: Any = parse_header(ctx, line.tokens[:colon + 1])
    node.body = parse_body(ctx, line, colon, "'with'")
    return ([node], index + 1)
