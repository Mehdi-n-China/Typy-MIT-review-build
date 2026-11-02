"""Structural rules for a typed parameter list."""
from typing import Any
from .. import tools
from ..tree import ParameterKind
from ._errors import syntax_error
from ._context import ParseContext

def validate_parameters(ctx: ParseContext, parameters: list, token: tools.tokens.TokenInfo) -> None:
    """Raise unless ``parameters`` form a legal Python-style list.

    Mirrors what Python enforces for ``def``: no duplicate names, ``/`` only
    after at least one positional parameter and before any ``*``, a bare ``*``
    needs keyword-only parameters after it, ``**`` comes last, and a
    positional parameter without a default may not follow one with a default.
    """
    seen: set = set()
    star_seen: bool = False
    default_seen: bool = False
    positional_count: int = 0
    for position, parameter in enumerate(parameters):
        kind: Any = parameter.kind
        if not parameter.is_marker:
            if parameter.name in seen:
                raise syntax_error(ctx, f'duplicate parameter name \'{parameter.name}\'', token)
            seen.add(parameter.name)
        if kind == ParameterKind.SLASH:
            if star_seen:
                raise syntax_error(ctx, "'/' must come before '*'", token)
            if positional_count == 0:
                raise syntax_error(ctx, "'/' needs at least one parameter before it", token)
        elif kind in (ParameterKind.STAR, ParameterKind.VARARG):
            if star_seen:
                raise syntax_error(ctx, "only one '*' or '*type name' parameter is allowed", token)
            star_seen = True
            if kind == ParameterKind.STAR and (not any((p.kind == ParameterKind.NORMAL for p in parameters[position + 1:]))):
                raise syntax_error(ctx, "'*' must be followed by at least one keyword-only parameter", token)
        elif kind == ParameterKind.KWARG:
            if position != len(parameters) - 1:
                raise syntax_error(ctx, "the '**' parameter must be last", token)
        elif kind == ParameterKind.NORMAL and (not star_seen):
            positional_count += 1
            if parameter.default is not None:
                default_seen = True
            elif default_seen:
                raise syntax_error(ctx, f'parameter \'{parameter.name}\' has no default but follows one that does', token)
