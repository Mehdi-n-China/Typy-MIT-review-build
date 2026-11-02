"""``InitializedLoop`` -> init, ``try`` / ``while`` / ``finally: del``."""
from typing import Any
from .. import tools
from ._negate import negate
from ._walk import lower_list, lower_node
from ..context import CompileContext
_PYAST: tools.types.ModuleType = tools.pyast

def lower_initialized_loop(node: Any, ctx: CompileContext) -> list:
    """``i(0) while i < 3:`` becomes::

        i: Any = 0
        try:
            while i < 3:
                ...
        finally:
            del i

    The variables are declared ``dyn`` (shown as ``Any``) and deleted however
    the loop ends, including ``break`` and exceptions (spec §17). ``until``
    negates the test. The ``else`` block stays attached to the ``while``.
    """
    ctx.uses_any = True
    statements: list = [_PYAST.AnnAssign(target=_PYAST.Name(id=binding.name, ctx=_PYAST.Store()), annotation=_PYAST.Name(id='Any', ctx=_PYAST.Load()), value=lower_node(binding.value, ctx), simple=1) for binding in node.bindings]
    test: Any = lower_node(node.test, ctx)
    if node.mode == 'until':
        test = negate(test)
    loop: _PYAST.While = _PYAST.While(test=test, body=lower_list(node.body, ctx), orelse=lower_list(node.orelse, ctx))
    cleanup: _PYAST.Delete = _PYAST.Delete(targets=[_PYAST.Name(id=binding.name, ctx=_PYAST.Del()) for binding in node.bindings])
    statements.append(_PYAST.Try(body=[loop], handlers=[], orelse=[], finalbody=[cleanup]))
    return [_PYAST.copy_location(statement, node) for statement in statements]
