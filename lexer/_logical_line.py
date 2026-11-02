"""One logical line of source plus the indented block beneath it."""
from typing import Any
from .. import tools

class LogicalLine:
    """The significant tokens of one logical line (comments and blank lines
    removed) and, if an indented block follows it, that block's lines."""
    __slots__: tuple = ('tokens', 'children')

    def __init__(self: LogicalLine, tokens: list) -> None:
        self.tokens = tokens
        self.children = []

    @property
    def first(self: LogicalLine) -> tools.tokens.TokenInfo:
        return self.tokens[0]

    @property
    def last(self: LogicalLine) -> tools.tokens.TokenInfo:
        return self.tokens[-1]

    @property
    def line(self: LogicalLine) -> Any:
        return self.tokens[0].start[0]

    @property
    def col(self: LogicalLine) -> Any:
        return self.tokens[0].start[1]
