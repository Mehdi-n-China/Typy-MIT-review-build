"""One step of a lowered optional chain."""
from typing import Any
from .. import tools
from ..context import CompileContext
from ._walk import lower_node
_PYAST: tools.types.ModuleType = tools.pyast

def apply_link(target: Any, link: Any, ctx: CompileContext) -> Any:
    """The single access ``link`` performs on ``target``."""
    if link.kind == 'attr':
        return _PYAST.Attribute(value=target, attr=link.name, ctx=_PYAST.Load())
    if link.kind == 'sub':
        return _PYAST.Subscript(value=target, slice=lower_node(link.index, ctx), ctx=_PYAST.Load())
    return _PYAST.Call(func=target, args=[lower_node(argument, ctx) for argument in link.args], keywords=[lower_node(keyword, ctx) for keyword in link.keywords])
