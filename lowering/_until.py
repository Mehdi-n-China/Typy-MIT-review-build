"""``UntilLoop`` -> ``while not ...``."""
from typing import Any
from .. import tools
from ._negate import negate
from ._walk import lower_list, lower_node
from ..context import CompileContext
_PYAST: tools.types.ModuleType = tools.pyast

def lower_until(node: Any, ctx: CompileContext) -> list:
    """``until test:`` is ``while not test:``; ``else`` is unchanged."""
    lowered: _PYAST.While = _PYAST.While(test=negate(lower_node(node.test, ctx)), body=lower_list(node.body, ctx), orelse=lower_list(node.orelse, ctx))
    return [_PYAST.copy_location(lowered, node)]
