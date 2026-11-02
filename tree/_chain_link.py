"""One step of an optional-chaining expression."""
from typing import Any
from ._base import TypyNode

class ChainLink(TypyNode):
    """A single postfix operation in a chain such as ``a?.b[c](d)``.

    ``kind`` is ``"attr"`` (uses ``name``), ``"sub"`` (uses ``index``) or
    ``"call"`` (uses ``args`` / ``keywords``). ``guarded`` is true when the
    step was written with a leading ``?``: if the value it would operate on
    is ``None``, the whole rest of the chain is skipped and the expression
    evaluates to ``None``.
    """
    _fields: tuple = ('kind', 'guarded', 'name', 'index', 'args', 'keywords')

    def __init__(self: ChainLink, kind: str='attr', guarded: bool=False, name: Any=None, index: Any=None, args: Any=None, keywords: Any=None) -> None:
        self.kind = kind
        self.guarded = guarded
        self.name = name
        self.index = index
        self.args = args if args is not None else []
        self.keywords = keywords if keywords is not None else []
