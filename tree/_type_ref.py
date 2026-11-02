"""A reference to a type as written in Typy source."""
from typing import Any
from .. import tools
from ._base import TypyNode

class TypeRef(TypyNode):
    """A (possibly dotted) type name: ``int``, ``Car``, ``Parent.Car``...

    ``parts`` holds the dotted segments. The parser never checks that a type
    exists (spec §5: ``Car x = Not_A_Car()`` is syntactically fine), so this
    is purely a name.
    """
    _fields: tuple = ('parts',)

    def __init__(self: TypeRef, parts: Any=None) -> None:
        self.parts = list(parts) if parts else []

    @property
    def text(self: TypeRef) -> str:
        """The type as written, e.g. ``"Parent.Car"``."""
        return '.'.join(self.parts)

    @property
    def is_any(self: TypeRef) -> bool:
        return self.parts == ['any']

    @property
    def is_dyn(self: TypeRef) -> bool:
        return self.parts == ['dyn']

    @property
    def is_void(self: TypeRef) -> bool:
        return self.parts == ['void']

    @property
    def is_none(self: TypeRef) -> bool:
        return self.parts == ['None']

    @property
    def is_pseudo(self: TypeRef) -> bool:
        """``any``, ``dyn`` or ``void``: Typy's own types, never real classes."""
        return self.is_any or self.is_dyn or self.is_void

    def to_expression(self: TypeRef) -> Any:
        """The plain Python expression for this type: ``Name`` / ``Attribute``
        chain, or the constant ``None`` for the type ``None``."""
        if self.is_none:
            return tools.pyast.Constant(value=None)
        node: Any = tools.pyast.Name(id=self.parts[0], ctx=tools.pyast.Load())
        for part in self.parts[1:]:
            node = tools.pyast.Attribute(value=node, attr=part, ctx=tools.pyast.Load())
        return node

    def __repr__(self: TypeRef) -> str:
        return f'TypeRef({self.text!r})'
