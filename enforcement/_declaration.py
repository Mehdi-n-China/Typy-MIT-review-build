"""Enforcing typed declarations."""
from typing import Any
from .. import tools
from ..semantics import BindingKind
from ._any_state import any_state_statement
from ._checked_value import checked_value
from ..context import CompileContext

def enforce_declaration(statement: Any, ctx: CompileContext) -> list:
    """Wrap the value of a typed declaration (``int x = ...`` or ``x: int = ...``)
    in its runtime check. Returns the statements that replace it: for an
    ``any`` declaration that includes the state-variable assignment before it.
    """
    value: Any = getattr(statement, 'value', None)
    binding: Any = getattr(statement, 'binding', None)
    if value is None or binding is None:
        return [statement]
    name: Any = statement.name if hasattr(statement, 'name') else statement.target.id
    prologue: list = []
    if binding.kind == BindingKind.ANY:
        prologue.append(any_state_statement(binding, ctx))
    statement.value = checked_value(value, binding, name, ctx)
    return prologue + [statement]
