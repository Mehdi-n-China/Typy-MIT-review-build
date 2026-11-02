"""``RepeatLoop`` -> ``for __ in range(...)``."""
from typing import Any
from .. import tools
from ..reserved import REPEAT_VARIABLE
from ._walk import lower_list, lower_node
from ..context import CompileContext
_PYAST: tools.types.ModuleType = tools.pyast

def lower_repeat(node: Any, ctx: CompileContext) -> list:
    """``repeat n:`` is ``for __ in range(n):`` (spec §21). ``__`` is the
    compiler-owned throwaway name: it is reserved, so user code can never
    collide with it or read it."""
    lowered: _PYAST.For = _PYAST.For(target=_PYAST.Name(id=REPEAT_VARIABLE, ctx=_PYAST.Store()), iter=_PYAST.Call(func=_PYAST.Name(id='range', ctx=_PYAST.Load()), args=[lower_node(node.count, ctx)], keywords=[]), body=lower_list(node.body, ctx), orelse=lower_list(node.orelse, ctx), type_comment=None)
    return [_PYAST.copy_location(lowered, node)]
