"""The signature of a typed function."""
from typing import Any
from ._base import TypyNode

class Signature(TypyNode):
    """``parameters`` (a list of ``Parameter``) and the ``returns`` ``TypeRef``.

    Typy requires both (spec §15): every parameter is typed and every function
    has an explicit return type, ``void`` and ``None`` included.
    """
    _fields: tuple = ('parameters', 'returns')

    def __init__(self: Signature, parameters: Any=None, returns: Any=None) -> None:
        self.parameters = list(parameters) if parameters else []
        self.returns = returns
