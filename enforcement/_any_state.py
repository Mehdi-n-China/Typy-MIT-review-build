"""The hidden variable that remembers an ``any`` binding's type."""
from typing import Any
from .. import tools
from ._calls import runtime_call
from ..context import CompileContext
_PYAST: tools.types.ModuleType = tools.pyast

def any_state_statement(binding: Any, ctx: CompileContext) -> _PYAST.Assign:
    """``_typy_state_N = typy.AnyState()`` for an ``any`` binding.

    Emitted right before the declaration, so every execution of the
    declaration starts from a blank slate and the first value assigned
    establishes the type (spec §10).
    """
    return _PYAST.Assign(targets=[_PYAST.Name(id=binding.state_var, ctx=_PYAST.Store())], value=runtime_call(ctx, 'AnyState', []))
