"""A block of statements: the unit the whole parser recurses on."""
from typing import Any
from ._classify import classify_line
from ._decorator import parse_decorator
from ._dispatch import DECORATABLE, PARSERS
from ._errors import syntax_error
from ..lexer import LogicalLine
from ._context import ParseContext

def parse_block(ctx: ParseContext, lines: list) -> list:
    """Parse sibling logical lines into a list of statement nodes.

    Decorator lines are collected and handed to the function or class that
    follows them. Each statement parser consumes as many lines as it needs
    (an ``if`` takes its ``elif`` / ``else`` lines too) and returns the index
    of the next unread line.
    """
    statements: list = []
    decorators: list = []
    index: int = 0
    while index < len(lines):
        line: LogicalLine = lines[index]
        kind: str = classify_line(line)
        if kind == 'decorator':
            decorators.append(parse_decorator(ctx, line))
            index += 1
            continue
        if decorators and kind not in DECORATABLE:
            raise syntax_error(ctx, 'a decorator must be followed by a function or class', line.first)
        nodes: Any = None
        nodes, index = PARSERS[kind](ctx, lines, index, decorators)
        decorators = []
        statements.extend(nodes)
    if decorators:
        raise syntax_error(ctx, 'a decorator must be followed by a function or class', lines[-1].last)
    return statements
