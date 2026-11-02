"""``try`` / ``except`` / ``else`` / ``finally``."""
from typing import Any
from .. import tools
from ..tree import place
from ._header_stub import parse_header
from ._body import parse_body, require_header_colon
from ._else_clause import parse_else_clause
from ._errors import syntax_error
from ._keywords import starts_with
from ..lexer import LogicalLine
from ._context import ParseContext
_TRY_STAR: Any = getattr(tools.pyast, 'TryStar', None)

def _parse_handler(ctx: ParseContext, line: LogicalLine) -> tuple:
    """Parse an ``except ...:`` header inside a stub ``try`` and return
    ``(handler_node, is_star, colon_index)``."""
    colon: int = require_header_colon(ctx, line, 'except')
    stub: Any = parse_header(ctx, line.tokens[:colon + 1], prefix='try: pass\n')
    is_star: bool = _TRY_STAR is not None and isinstance(stub, _TRY_STAR)
    return (stub.handlers[0], is_star, colon)

def parse_try(ctx: ParseContext, lines: list, index: int, decorators: list) -> tuple:
    """Parse a whole ``try`` statement and its clauses."""
    line: LogicalLine = lines[index]
    colon: int = require_header_colon(ctx, line, 'try')
    if colon != 1:
        raise syntax_error(ctx, "'try' does not take a condition", line.tokens[1])
    body: list = parse_body(ctx, line, colon, "'try'")
    index += 1
    handlers: Any = None
    star_flags: Any = None
    handlers, star_flags = ([], set())
    while index < len(lines) and starts_with(lines[index], 'except'):
        handler_line: LogicalLine = lines[index]
        handler: Any = None
        is_star: Any = None
        handler_colon: Any = None
        handler, is_star, handler_colon = _parse_handler(ctx, handler_line)
        handler.body = parse_body(ctx, handler_line, handler_colon, "'except'")
        handlers.append(handler)
        star_flags.add(is_star)
        index += 1
    if len(star_flags) > 1:
        raise syntax_error(ctx, "cannot mix 'except' and 'except*' in one 'try'", line.first)
    orelse: list = []
    if handlers:
        orelse, index = parse_else_clause(ctx, lines, index)
    finalbody: list = []
    if index < len(lines) and starts_with(lines[index], 'finally'):
        final_line: LogicalLine = lines[index]
        final_colon: int = require_header_colon(ctx, final_line, 'finally')
        finalbody = parse_body(ctx, final_line, final_colon, "'finally'")
        index += 1
    if not handlers and (not finalbody):
        raise syntax_error(ctx, "'try' needs at least one 'except' or a 'finally'", line.first)
    node_type: Any = _TRY_STAR if star_flags == {True} else tools.pyast.Try
    node: Any = node_type(body=body, handlers=handlers, orelse=orelse, finalbody=finalbody)
    return ([place(node, line.first, line.tokens[colon])], index)
