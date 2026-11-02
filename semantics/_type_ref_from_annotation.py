"""Reading a Python annotation expression back as a Typy type."""
from typing import Any
from .. import tools
from ..tree import TypeRef

def type_ref_from_annotation(node: Any) -> Any:
    """``TypeRef`` for a dotted-name annotation (``int``, ``Parent.Car``) or
    the constant ``None``; ``None`` for anything else (``list[int]``...).

    Typy only enforces types it can name, so complex annotations are left to
    Python.
    """
    if isinstance(node, tools.pyast.Constant) and node.value is None:
        return TypeRef(['None'])
    parts: list = []
    while isinstance(node, tools.pyast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, tools.pyast.Name):
        parts.append(node.id)
        return TypeRef(list(reversed(parts)))
    return None
