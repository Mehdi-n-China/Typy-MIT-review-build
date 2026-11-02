"""A logical line of simple statements."""
from ._errors import indentation_error
from ._segments import parse_segments
from ..lexer import LogicalLine
from ._context import ParseContext

def parse_simple_line(ctx: ParseContext, lines: list, index: int, decorators: list) -> tuple:
    """Parse ``lines[index]`` as simple statement(s); a simple statement can
    never own an indented block."""
    line: LogicalLine = lines[index]
    if line.children:
        raise indentation_error(ctx, 'unexpected indent', line.children[0].first)
    return (parse_segments(ctx, line.tokens), index + 1)
