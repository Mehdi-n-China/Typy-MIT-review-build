"""``TYPE name = value`` declarations (spec §5)."""
from typing import Any
from .. import tools
from ..lexer import read_dotted_name
from ..reserved import PY_HARD_KEYWORDS
from ..tree import TypedDeclaration, TypeRef, place
from ._bridge import parse_python_expression
from ._errors import syntax_error
from ._context import ParseContext

def match_typed_declaration(tokens: list) -> Any:
    """Recognise ``TYPE name =`` at the start of ``tokens``.

    Two names in a row followed by ``=`` is never valid Python (not even a
    soft keyword produces it), so this pattern is unambiguous. Returns
    ``(type_parts, name_token, equals_index)`` or ``None``.
    """
    parsed: Any = read_dotted_name(tokens, 0)
    if parsed is None:
        return None
    after_type: Any = None
    parts: Any = None
    after_type, parts = parsed
    if after_type + 1 >= len(tokens):
        return None
    name: tools.tokens.TokenInfo = tokens[after_type]
    equals: tools.tokens.TokenInfo = tokens[after_type + 1]
    if name.type != tools.tokens.NAME or name.string in PY_HARD_KEYWORDS:
        return None
    if equals.type != tools.tokens.OP or equals.string != '=':
        return None
    return (parts, name, after_type + 1)

def parse_typed_declaration(ctx: ParseContext, tokens: list, match: Any) -> TypedDeclaration:
    """Build a ``TypedDeclaration`` from tokens that ``match`` recognised."""
    parts: Any = None
    name: Any = None
    equals_index: Any = None
    parts, name, equals_index = match
    if parts == ['void']:
        raise syntax_error(ctx, "'void' is only valid as a function return type", tokens[0], hint="declare a variable with a real type, or use 'dyn' if it may hold anything")
    value_tokens: list = tokens[equals_index + 1:]
    if not value_tokens:
        raise syntax_error(ctx, f'expected a value after \'=\' in the declaration of \'{name.string}\'', tokens[equals_index])
    value: Any = parse_python_expression(ctx, value_tokens)
    type_ref: Any = place(TypeRef(parts), tokens[0], tokens[equals_index - 2])
    return place(TypedDeclaration(type_ref, name.string, value), tokens[0], tokens[-1])
