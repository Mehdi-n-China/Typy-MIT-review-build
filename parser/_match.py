"""``match`` / ``case`` (a soft keyword, so it is probed before it is trusted)."""
from typing import Any
from .. import tools
from ..lexer import find_header_colon, LogicalLine
from ._guards import segment_text
from ._header_stub import parse_header
from ._body import parse_body
from ._errors import syntax_error
from ._keywords import starts_with
from ._simple import parse_simple_line
from ._context import ParseContext
_CASE_STUB: str = '\n case _: pass'

def _is_match_statement(ctx: ParseContext, line: LogicalLine) -> bool:
    """True if ``line`` is really a ``match subject:`` header.

    ``match`` is only a keyword here; ``match = re.match(...)`` is an
    assignment. A cheap shape test comes first, then a quiet trial parse.
    """
    if not line.children or find_header_colon(line.tokens, 1) != len(line.tokens) - 1:
        return False
    try:
        tree: Any = tools.pyast.parse(segment_text(ctx, line.tokens) + _CASE_STUB)
    except SyntaxError:
        return False
    return isinstance(tree.body[0], tools.pyast.Match)

def parse_match(ctx: ParseContext, lines: list, index: int, decorators: list) -> tuple:
    """Parse a ``match`` statement; anything that is not one is handed to the
    simple-statement parser, which will parse (or reject) it as Python."""
    line: LogicalLine = lines[index]
    if not _is_match_statement(ctx, line):
        return parse_simple_line(ctx, lines, index, decorators)
    node: Any = parse_header(ctx, line.tokens, suffix=_CASE_STUB)
    cases: list = []
    for case_line in line.children:
        if not starts_with(case_line, 'case'):
            raise syntax_error(ctx, "only 'case' clauses may appear directly inside 'match'", case_line.first)
        colon: Any = find_header_colon(case_line.tokens, 1)
        if colon is None:
            raise syntax_error(ctx, "expected ':' at the end of the 'case' header", case_line.last)
        stub: Any = parse_header(ctx, case_line.tokens[:colon + 1], prefix='match _:\n ', col_shift=-1)
        case: Any = stub.cases[0]
        case.body = parse_body(ctx, case_line, colon, "'case'")
        cases.append(case)
    node.cases = cases
    return ([node], index + 1)
