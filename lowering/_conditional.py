"""``Conditional`` -> a chain of ``if`` / ``elif`` / ``else``."""
from typing import Any
from .. import tools
from ..context import CompileContext
from ._negate import negate
from ._walk import lower_list, lower_node
_PYAST: tools.types.ModuleType = tools.pyast

def lower_conditional(node: Any, ctx: CompileContext) -> list:
    """Build the chain from the last branch backwards so each ``if`` owns the
    rest of the chain as its ``orelse``; Python prints nested single ``if``s
    in an ``orelse`` as ``elif``. ``unless`` / ``elunless`` negate the test."""
    orelse: list = lower_list(node.orelse, ctx)
    for branch in reversed(node.branches):
        test: Any = lower_node(branch.test, ctx)
        if branch.negated:
            test = negate(test)
        lowered: _PYAST.If = _PYAST.If(test=test, body=lower_list(branch.body, ctx), orelse=orelse)
        orelse = [_PYAST.copy_location(lowered, branch)]
    return orelse
