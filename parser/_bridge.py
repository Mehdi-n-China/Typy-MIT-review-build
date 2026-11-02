"""Handing ordinary Python syntax to Python's own parser.

Typy only parses what Typy adds. Every plain statement and every expression
is cut out of the source as exact text and parsed by ``ast.parse``: that is
how "Typy behaves exactly like Python except where specified" stays true.
"""
from typing import Any
from ._guards import segment_text
from ._parse_text import parse_python_text
from ._context import ParseContext

def parse_python_statements(ctx: ParseContext, tokens: list) -> list:
    """Parse the tokens of one simple statement into a list of Python
    statement nodes."""
    return parse_python_text(ctx, segment_text(ctx, tokens), 'exec', tokens[0]).body

def parse_python_expression(ctx: ParseContext, tokens: list) -> Any:
    """Parse the tokens of one expression into a Python expression node.

    The text is wrapped in parentheses so multi-line expressions, bare tuples
    and leading whitespace all parse the way they would inside a statement.
    """
    text: str = '(' + segment_text(ctx, tokens) + ')'
    return parse_python_text(ctx, text, 'eval', tokens[0], col_shift=-1).body
