"""Wrapping a value in the runtime check its binding calls for."""
from typing import Any
from .. import tools
from ..semantics import BindingKind
from ._calls import runtime_call, runtime_type_expression
from ..context import CompileContext
_PYAST: tools.types.ModuleType = tools.pyast

def checked_value(value: Any, binding: Any, name: str, ctx: CompileContext) -> Any:
    """``value`` wrapped in ``typy.check(...)`` / ``typy.check_any(...)``
    according to ``binding``; unchanged for ``dyn`` and untyped bindings
    (``dyn`` skips enforcement entirely, spec §11).
    """
    if binding is None:
        return value
    if binding.kind == BindingKind.CONCRETE:
        return runtime_call(ctx, 'check', [value, runtime_type_expression(binding.type_ref), _PYAST.Constant(value=name)])
    if binding.kind == BindingKind.ANY:
        state: _PYAST.Name = _PYAST.Name(id=binding.state_var, ctx=_PYAST.Load())
        return runtime_call(ctx, 'check_any', [value, state, _PYAST.Constant(value=name)])
    return value
