"""Decorator lines (``@expression``)."""
from typing import Any
from ._bridge import parse_python_expression
from ._errors import indentation_error, syntax_error
from ..lexer import LogicalLine
from ._context import ParseContext

def parse_decorator(ctx: ParseContext, line: LogicalLine) -> Any:
    """Parse one ``@expression`` line and return the expression node."""
    if line.children:
        raise indentation_error(ctx, 'unexpected indent', line.children[0].first)
    if len(line.tokens) < 2:
        raise syntax_error(ctx, "expected an expression after '@'", line.first)
    return parse_python_expression(ctx, line.tokens[1:])
