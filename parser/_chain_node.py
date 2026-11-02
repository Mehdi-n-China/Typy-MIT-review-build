"""Building an ``OptionalChain`` from an unwound postfix chain."""
from typing import Any
from .. import tools
from ..errors import TypyChainError
from ..tree import ChainLink, OptionalChain
from ._chain_postfix import is_guard_marker

def _error(message: str, node: Any, filename: str) -> TypyChainError:
    return TypyChainError(message, node.lineno, node.col_offset, filename)

def build_chain_node(outer: Any, links: list, base: Any, rewrite: tools.types.FunctionType, filename: str) -> OptionalChain:
    """Rebuild the chain ``links`` (innermost first) over ``base`` as an
    ``OptionalChain``.

    A marker attribute guards the link right after it. ``rewrite`` is
    ``build_optional_chains`` (passed in to avoid a circular import) and is
    applied to every nested expression: the base, subscript keys, call
    arguments. Chains cannot be assignment/deletion targets and a call can
    never be guarded, because ``?`` only attaches to ``.`` and ``[``.
    """
    if not isinstance(getattr(outer, 'ctx', tools.pyast.Load()), tools.pyast.Load):
        raise _error('optional chaining cannot be used as an assignment or deletion target', outer, filename)
    chain_links: list = []
    guarded: bool = False
    for link in links:
        if is_guard_marker(link):
            guarded = True
            continue
        if isinstance(link, tools.pyast.Attribute):
            built: ChainLink = ChainLink('attr', guarded, name=link.attr)
        elif isinstance(link, tools.pyast.Subscript):
            built = ChainLink('sub', guarded, index=rewrite(link.slice))
        else:
            if guarded:
                raise _error("'?' cannot be applied to a call", link, filename)
            built = ChainLink('call', False, args=[rewrite(argument) for argument in link.args], keywords=[rewrite(keyword) for keyword in link.keywords])
        chain_links.append(tools.pyast.copy_location(built, link))
        guarded = False
    if guarded:
        raise _error("'?.' must be followed by an attribute name", outer, filename)
    return tools.pyast.copy_location(OptionalChain(rewrite(base), chain_links), outer)
