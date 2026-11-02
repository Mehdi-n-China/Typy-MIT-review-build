"""Class definitions, which are plain Python in Typy."""
from typing import Any
from ._header_stub import parse_header
from ._body import parse_body, require_header_colon
from ..lexer import LogicalLine
from ._context import ParseContext

def parse_class(ctx: ParseContext, lines: list, index: int, decorators: list) -> tuple:
    """Parse ``class Name(bases):`` with Python's parser; the body is parsed
    as Typy, so typed declarations and typed methods work inside classes."""
    line: LogicalLine = lines[index]
    colon: int = require_header_colon(ctx, line, 'class')
    node: Any = parse_header(ctx, line.tokens[:colon + 1])
    node.decorator_list = list(decorators)
    node.body = parse_body(ctx, line, colon, f'class \'{node.name}\'')
    return ([node], index + 1)
