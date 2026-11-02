"""``if`` / ``unless`` chains (spec §22-23)."""
from typing import Any
from .. import tools
from ..tree import Branch, Conditional, place
from ._bridge import parse_python_expression
from ._body import parse_body, require_header_colon
from ._else_clause import parse_else_clause
from ._errors import syntax_error
from ..lexer import LogicalLine
from ._context import ParseContext
_CONTINUATIONS: tuple = ('elif', 'elunless')

def _continues(lines: list, index: int) -> bool:
    if index >= len(lines):
        return False
    first: tools.tokens.TokenInfo = lines[index].first
    return first.type == tools.tokens.NAME and first.string in _CONTINUATIONS

def parse_conditional(ctx: ParseContext, lines: list, index: int, decorators: list) -> tuple:
    """Parse an ``if`` or ``unless`` line plus any ``elif`` / ``elunless``
    lines and a closing ``else`` into one ``Conditional``.

    Python's ``elif`` and Typy's ``elunless`` may follow either opener in any
    order: each branch only means "test this, negated or not".
    """
    opener: LogicalLine = lines[index]
    branches: list = []
    while True:
        line: LogicalLine = lines[index]
        keyword: str = line.first.string
        colon: int = require_header_colon(ctx, line, keyword)
        test_tokens: list = line.tokens[1:colon]
        if not test_tokens:
            raise syntax_error(ctx, f'\'{keyword}\' needs a condition', line.first)
        test: Any = parse_python_expression(ctx, test_tokens)
        body: list = parse_body(ctx, line, colon, f'\'{keyword}\'')
        branches.append(place(Branch(keyword, test, body), line.first, line.tokens[colon]))
        index += 1
        if not _continues(lines, index):
            break
    orelse: Any = None
    orelse, index = parse_else_clause(ctx, lines, index)
    return ([place(Conditional(branches, orelse), opener.first, opener.last)], index)
