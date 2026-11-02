"""Rebuilding optional-chaining nodes after Python has parsed the snippet."""
from typing import Any
from .. import tools
from ._chain_node import build_chain_node
from ._chain_postfix import POSTFIX, is_guard_marker, unwind_postfix

def build_optional_chains(node: Any, filename: str='<typy>') -> Any:
    """Replace every guarded postfix chain inside ``node`` with an
    ``OptionalChain`` and return the (possibly new) node.

    Chains without a guard marker are left exactly as Python parsed them;
    ``filename`` is only used to locate errors.
    """
    rewrite: tools.types.FunctionType = lambda child: build_optional_chains(child, filename)
    if isinstance(node, POSTFIX):
        links: Any = None
        base: Any = None
        links, base = unwind_postfix(node)
        if any((is_guard_marker(link) for link in links)):
            return build_chain_node(node, links, base, rewrite, filename)
    for name, value in tools.pyast.iter_fields(node):
        if isinstance(value, list):
            value[:] = [rewrite(item) if isinstance(item, tools.pyast.AST) else item for item in value]
        elif isinstance(value, tools.pyast.AST):
            setattr(node, name, rewrite(value))
    return node
