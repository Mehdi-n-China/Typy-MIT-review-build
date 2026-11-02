"""``TYPE name = value``."""
from typing import Any
from ._base import TypyStatement

class TypedDeclaration(TypyStatement):
    """A typed variable declaration such as ``int x = 10`` (spec §5).

    ``type`` is a ``TypeRef``, ``name`` the declared identifier and ``value``
    the initial value expression. Lowers to an annotated assignment.
    """
    _fields: tuple = ('type', 'name', 'value')

    def __init__(self: TypedDeclaration, type: Any=None, name: Any=None, value: Any=None) -> None:
        self.type = type
        self.name = name
        self.value = value
