"""Parsing the parenthesised parameter list of a typed function."""
from typing import Any
from .. import tools
from ..lexer import read_dotted_name, split_top_level
from ..reserved import PY_HARD_KEYWORDS
from ..tree import Parameter, ParameterKind, TypeRef, place
from ._bridge import parse_python_expression
from ._errors import syntax_error
from ._keywords import is_op
from ._validate_parameters import validate_parameters
from ._context import ParseContext

def _parse_one(ctx: ParseContext, group: list) -> Parameter:
    head: tools.tokens.TokenInfo = group[0]
    if len(group) == 1 and is_op(head, '/'):
        return place(Parameter('/', None, None, ParameterKind.SLASH), head)
    if len(group) == 1 and is_op(head, '*'):
        return place(Parameter('*', None, None, ParameterKind.STAR), head)
    kind: Any = None
    start: Any = None
    kind, start = (ParameterKind.NORMAL, 0)
    if is_op(head, '*'):
        kind, start = (ParameterKind.VARARG, 1)
    elif is_op(head, '**'):
        kind, start = (ParameterKind.KWARG, 1)
    parsed: Any = read_dotted_name(group, start)
    if parsed is None:
        raise syntax_error(ctx, 'every parameter needs a type before its name', head, hint="e.g. 'int count', '*str names', or 'dyn value' if the type can vary")
    after_type: Any = None
    parts: Any = None
    after_type, parts = parsed
    if after_type >= len(group) or group[after_type].type != tools.tokens.NAME or group[after_type].string in PY_HARD_KEYWORDS:
        raise syntax_error(ctx, 'expected a parameter name after the type', group[min(after_type, len(group) - 1)])
    if parts == ['void']:
        raise syntax_error(ctx, "'void' cannot be used as a parameter type", head)
    name: tools.tokens.TokenInfo = group[after_type]
    rest: list = group[after_type + 1:]
    default: Any = None
    if rest:
        if kind != ParameterKind.NORMAL or not is_op(rest[0], '='):
            raise syntax_error(ctx, 'unexpected tokens in parameter', rest[0])
        if len(rest) == 1:
            raise syntax_error(ctx, f'expected a default value after \'=\' for \'{name.string}\'', rest[0])
        default = parse_python_expression(ctx, rest[1:])
    type_ref: Any = place(TypeRef(parts), group[start], group[after_type - 1])
    return place(Parameter(name.string, type_ref, default, kind), head, group[-1])

def parse_parameters(ctx: ParseContext, tokens: list, signature_token: tools.tokens.TokenInfo) -> list:
    """Parse the tokens between a signature's parentheses into a list of
    ``Parameter`` nodes and validate their structure."""
    parameters: list = []
    for group in split_top_level(tokens, ','):
        if not group:
            raise syntax_error(ctx, 'empty parameter', signature_token)
        parameters.append(_parse_one(ctx, group))
    validate_parameters(ctx, parameters, signature_token)
    return parameters
