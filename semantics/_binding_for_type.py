"""Choosing the binding kind a declared type implies."""
from typing import Any
from ..tree import TypeRef
from ._binding import Binding, BindingKind
from ._literal_type_of import literal_type_of
from ..context import CompileContext

def binding_for_type(type_ref: Any, ctx: CompileContext, value: Any=None) -> Binding:
    """The ``Binding`` that declaring a name with ``type_ref`` creates.

    ``any`` normally gets a hidden state variable so the first runtime value
    can fix the type. When the initial ``value`` is a literal, that type is
    already known, so the binding is resolved right here at compile time and
    behaves exactly like a declaration of the literal's type. ``dyn`` is never
    enforced; any other named type is checked exactly; no type means exempt.
    """
    if type_ref is None:
        return Binding(BindingKind.EXEMPT)
    if type_ref.is_any:
        literal: Any = literal_type_of(value) if value is not None else None
        if literal is not None:
            return Binding(BindingKind.CONCRETE, TypeRef([literal]))
        return Binding(BindingKind.ANY, type_ref, ctx.fresh_name('_typy_state_'))
    if type_ref.is_dyn:
        return Binding(BindingKind.DYN, type_ref)
    return Binding(BindingKind.CONCRETE, type_ref)
