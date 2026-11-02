"""Building Python's ``arguments`` object from Typy parameters."""
from typing import Any
from .. import tools
from ..context import CompileContext
from ..tree import Parameter, ParameterKind
from ._annotation import annotation_for
from ._walk import lower_node
_PYAST: tools.types.ModuleType = tools.pyast

def _argument(parameter: Parameter, ctx: CompileContext) -> tools.pyast.arg:
    node: Any = _PYAST.arg(arg=parameter.name, annotation=annotation_for(parameter.type, ctx), type_comment=None)
    return _PYAST.copy_location(node, parameter)

def build_arguments(parameters: list, ctx: CompileContext) -> tools.pyast.arguments:
    """Convert a Typy parameter list (markers included) into ``ast.arguments``.

    ``/`` moves everything collected so far into the positional-only group,
    a bare ``*`` or ``*type name`` starts the keyword-only group, and each
    default is lowered like any other expression.
    """
    positional_only: Any = None
    positional: Any = None
    keyword_only: Any = None
    positional_only, positional, keyword_only = ([], [], [])
    defaults: Any = None
    keyword_defaults: Any = None
    defaults, keyword_defaults = ([], [])
    vararg: Any = None
    kwarg: Any = None
    vararg = kwarg = None
    after_star: bool = False
    for parameter in parameters:
        kind: Any = parameter.kind
        if kind == ParameterKind.SLASH:
            positional_only, positional = (positional, [])
        elif kind == ParameterKind.STAR:
            after_star = True
        elif kind == ParameterKind.VARARG:
            vararg, after_star = (_argument(parameter, ctx), True)
        elif kind == ParameterKind.KWARG:
            kwarg = _argument(parameter, ctx)
        else:
            default: Any = lower_node(parameter.default, ctx) if parameter.default is not None else None
            if after_star:
                keyword_only.append(_argument(parameter, ctx))
                keyword_defaults.append(default)
            else:
                positional.append(_argument(parameter, ctx))
                if default is not None:
                    defaults.append(default)
    return _PYAST.arguments(posonlyargs=positional_only, args=positional, vararg=vararg, kwonlyargs=keyword_only, kw_defaults=keyword_defaults, kwarg=kwarg, defaults=defaults)
