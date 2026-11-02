"""How a name is bound, as far as Typy's type rules are concerned."""
from typing import Any

class BindingKind:
    """``EXEMPT``    bound by something untyped (loop target, import...): never enforced
    ``DYN``       declared ``dyn``: never enforced
    ``ANY``       declared ``any``: the first value fixes the type
    ``CONCRETE``  declared with a real type: always checked, exactly
    """
    EXEMPT: str = 'exempt'
    DYN: str = 'dyn'
    ANY: str = 'any'
    CONCRETE: str = 'concrete'

class Binding:
    """The Typy-level facts about one name at one point in a scope.

    ``type_ref`` is the declared ``TypeRef`` (``None`` for exempt bindings);
    ``state_var`` names the hidden variable holding an ``any`` binding's
    established type at runtime.
    """
    __slots__: tuple = ('kind', 'type_ref', 'state_var')

    def __init__(self: Binding, kind: Any, type_ref: Any=None, state_var: Any=None) -> None:
        self.kind = kind
        self.type_ref = type_ref
        self.state_var = state_var
