"""``ForeverLoop`` -> ``while True``."""
from typing import Any
from .. import tools
from ..context import CompileContext
from ._walk import lower_list
_PYAST: tools.types.ModuleType = tools.pyast

def lower_forever(node: Any, ctx: CompileContext) -> list:
    """``forever:`` is ``while True:``."""
    lowered: _PYAST.While = _PYAST.While(test=_PYAST.Constant(value=True), body=lower_list(node.body, ctx), orelse=lower_list(node.orelse, ctx))
    return [_PYAST.copy_location(lowered, node)]
