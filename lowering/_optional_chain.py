"""``OptionalChain`` -> nested conditional expressions."""
from typing import Any
from .. import tools
from ._chain_step import apply_link
from ._walk import lower_node
from ..context import CompileContext
_PYAST: tools.types.ModuleType = tools.pyast

def _render(current: Any, links: list, index: int, ctx: CompileContext) -> Any:
    """Build the expression for ``links[index:]`` applied to ``current``.

    A guarded link becomes ``None if (t := current) is None else <rest>``.
    The whole remainder of the chain lives in the ``else`` branch, so a
    ``None`` skips everything after it (further links, call arguments,
    subscript keys) without evaluating any of it: the chain is lazy.
    Unguarded links are plain Python and protect nothing.
    """
    if index == len(links):
        return current
    link: Any = links[index]
    if not link.guarded:
        return _render(apply_link(current, link, ctx), links, index + 1, ctx)
    temp: str = ctx.fresh_name('_typy_ch')
    rest: Any = _render(apply_link(_PYAST.Name(id=temp, ctx=_PYAST.Load()), link, ctx), links, index + 1, ctx)
    test: _PYAST.Compare = _PYAST.Compare(left=_PYAST.NamedExpr(target=_PYAST.Name(id=temp, ctx=_PYAST.Store()), value=current), ops=[_PYAST.Is()], comparators=[_PYAST.Constant(value=None)])
    return _PYAST.IfExp(test=test, body=_PYAST.Constant(value=None), orelse=rest)

def lower_optional_chain(node: Any, ctx: CompileContext) -> Any:
    """Lower an ``OptionalChain`` (spec §24)."""
    return _render(lower_node(node.base, ctx), node.links, 0, ctx)
