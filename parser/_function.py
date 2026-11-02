"""Typed function signatures: ``TYPE name(TYPE param, ...):`` (spec §15)."""
from typing import Any
from .. import tools
from ..lexer import find_closing_bracket, LogicalLine, read_dotted_name
from ..reserved import PY_HARD_KEYWORDS
from ..tree import FunctionDeclaration, Signature, TypeRef, place
from ._body import parse_body
from ._parameters import parse_parameters
from ._context import ParseContext

def match_function_declaration(tokens: list) -> Any:
    """Recognise ``[async] TYPE name(...) :``.

    A type name, then a second name, then ``(`` is never a Python call
    (``f(x)`` has one name, ``a.b(x)`` has none after the dotted part), so
    this is unambiguous. Returns ``(is_async, type_parts, name_index)`` or
    ``None``.
    """
    is_async: bool = tokens[0].type == tools.tokens.NAME and tokens[0].string == 'async'
    parsed: Any = read_dotted_name(tokens, 1 if is_async else 0)
    if parsed is None:
        return None
    after_type: Any = None
    parts: Any = None
    after_type, parts = parsed
    if after_type + 1 >= len(tokens):
        return None
    name: Any = None
    opener: Any = None
    name, opener = (tokens[after_type], tokens[after_type + 1])
    if name.type != tools.tokens.NAME or name.string in PY_HARD_KEYWORDS:
        return None
    if opener.type != tools.tokens.OP or opener.string != '(':
        return None
    close: int = find_closing_bracket(tokens, after_type + 1)
    colon: Any = tokens[close + 1] if close + 1 < len(tokens) else None
    if colon is None or colon.type != tools.tokens.OP or colon.string != ':':
        return None
    return (is_async, parts, after_type)

def parse_function_declaration(ctx: ParseContext, lines: list, index: int, decorators: list) -> tuple:
    """Parse a typed function and its body into a ``FunctionDeclaration``."""
    line: LogicalLine = lines[index]
    tokens: list = line.tokens
    is_async: Any = None
    parts: Any = None
    name_index: Any = None
    is_async, parts, name_index = match_function_declaration(tokens)
    open_index: Any = name_index + 1
    close_index: int = find_closing_bracket(tokens, open_index, ctx.filename)
    colon: int = close_index + 1
    parameters: list = parse_parameters(ctx, tokens[open_index + 1:close_index], tokens[name_index])
    first_type_index: int = 1 if is_async else 0
    returns: Any = place(TypeRef(parts), tokens[first_type_index], tokens[name_index - 1])
    signature: Any = place(Signature(parameters, returns), tokens[first_type_index], tokens[close_index])
    name: str = tokens[name_index].string
    body: list = parse_body(ctx, line, colon, f'function \'{name}\'')
    node: FunctionDeclaration = FunctionDeclaration(name, signature, body, list(decorators), is_async)
    return ([place(node, tokens[0], tokens[colon])], index + 1)
