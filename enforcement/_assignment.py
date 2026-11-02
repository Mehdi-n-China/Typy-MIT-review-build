"""Enforcing later assignments to typed names."""
from typing import Any
from .. import tools
from ..semantics import BindingKind
from ._checked_value import checked_value
from ..context import CompileContext
_PYAST: tools.types.ModuleType = tools.pyast

def enforce_assignment(statement: Any, ctx: CompileContext) -> list:
    """``x = value`` where ``x`` was declared: check ``value`` against the
    declared type (or the type ``any`` established). Only single plain-name
    targets are enforced.
    """
    binding: Any = getattr(statement, 'binding', None)
    if binding is not None:
        statement.value = checked_value(statement.value, binding, statement.targets[0].id, ctx)
    return [statement]

def enforce_augmented(statement: Any, ctx: CompileContext) -> list:
    """``x += value`` can change ``x``'s type (``int += float``), so the new
    value is re-checked in a statement that follows.
    """
    binding: Any = getattr(statement, 'binding', None)
    if binding is None or binding.kind not in (BindingKind.CONCRETE, BindingKind.ANY):
        return [statement]
    name: str = statement.target.id
    recheck: _PYAST.Assign = _PYAST.Assign(targets=[_PYAST.Name(id=name, ctx=_PYAST.Store())], value=checked_value(_PYAST.Name(id=name, ctx=_PYAST.Load()), binding, name, ctx))
    return [statement, recheck]
