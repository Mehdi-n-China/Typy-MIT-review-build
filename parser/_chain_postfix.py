"""Reading apart a postfix chain such as ``a.b[c](d)``."""
from typing import Any
from .. import tools
from ..reserved import CHAIN_GUARD
POSTFIX: tuple = (tools.pyast.Attribute, tools.pyast.Subscript, tools.pyast.Call)

def unwind_postfix(node: Any) -> tuple:
    """Split a postfix expression into ``(links, base)``.

    ``links`` lists the Attribute / Subscript / Call nodes from the innermost
    (applied first) to ``node`` itself; ``base`` is the non-postfix
    expression the chain starts from.
    """
    links: list = []
    current: Any = node
    while isinstance(current, POSTFIX):
        links.append(current)
        current = current.func if isinstance(current, tools.pyast.Call) else current.value
    links.reverse()
    return (links, current)

def is_guard_marker(node: Any) -> bool:
    """True for the marker attribute that ``segment_text`` put in place of ``?``."""
    return isinstance(node, tools.pyast.Attribute) and node.attr == CHAIN_GUARD
