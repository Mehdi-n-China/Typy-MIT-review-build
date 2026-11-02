"""``i(0) while cond:`` and ``i(0) until cond:`` (spec §17-18)."""
from typing import Any
from .. import tools
from ..lexer import find_closing_bracket, LogicalLine
from ..reserved import PY_HARD_KEYWORDS, STATEMENT_KEYWORDS
from ..tree import InitializedLoop, LoopBinding, place
from ._bridge import parse_python_expression
from ._body import parse_body, require_header_colon
from ._else_clause import parse_else_clause
from ._errors import syntax_error
from ._context import ParseContext

def match_initialized_loop(tokens: list) -> Any:
    """Recognise ``name(init)[, name2(init2)]* while|until`` at the start of
    ``tokens``. Returns ``(specs, keyword_index, mode)`` where each spec is
    ``(name_token, open_index, close_index)``, or ``None``.

    ``f(x)`` or ``f(x), g(y)`` on their own are ordinary expression
    statements; only the trailing ``while`` / ``until`` makes this a loop.
    """
    specs: list = []
    index: int = 0
    while True:
        if index + 1 >= len(tokens):
            return None
        name: Any = None
        opener: Any = None
        name, opener = (tokens[index], tokens[index + 1])
        if name.type != tools.tokens.NAME or name.string in PY_HARD_KEYWORDS or name.string in STATEMENT_KEYWORDS:
            return None
        if opener.type != tools.tokens.OP or opener.string != '(':
            return None
        close: int = find_closing_bracket(tokens, index + 1)
        specs.append((name, index + 1, close))
        after: int = close + 1
        if after < len(tokens) and tokens[after].type == tools.tokens.OP and (tokens[after].string == ','):
            index = after + 1
            continue
        break
    if after >= len(tokens) or tokens[after].type != tools.tokens.NAME or tokens[after].string not in ('while', 'until'):
        return None
    return (specs, after, tokens[after].string)

def parse_initialized_loop(ctx: ParseContext, lines: list, index: int, decorators: list) -> tuple:
    """Parse an initialized loop into an ``InitializedLoop``."""
    line: LogicalLine = lines[index]
    tokens: list = line.tokens
    specs: Any = None
    keyword_index: Any = None
    mode: Any = None
    specs, keyword_index, mode = match_initialized_loop(tokens)
    colon: int = require_header_colon(ctx, line, mode, start=keyword_index + 1)
    if colon == keyword_index + 1:
        raise syntax_error(ctx, f'\'{mode}\' needs a condition', tokens[keyword_index])
    bindings: list = []
    seen: set = set()
    for name, open_index, close_index in specs:
        if name.string in seen:
            raise syntax_error(ctx, f'loop variable \'{name.string}\' is initialized twice', name)
        seen.add(name.string)
        init_tokens: list = tokens[open_index + 1:close_index]
        if not init_tokens:
            raise syntax_error(ctx, f'loop variable \'{name.string}\' needs an initial value', name)
        value: Any = parse_python_expression(ctx, init_tokens)
        bindings.append(place(LoopBinding(name.string, value), name, tokens[close_index]))
    test: Any = parse_python_expression(ctx, tokens[keyword_index + 1:colon])
    body: list = parse_body(ctx, line, colon, f'\'{mode}\'')
    orelse: Any = None
    orelse, index = parse_else_clause(ctx, lines, index + 1)
    node: InitializedLoop = InitializedLoop(bindings, mode, test, body, orelse)
    return ([place(node, line.first, tokens[colon])], index)
