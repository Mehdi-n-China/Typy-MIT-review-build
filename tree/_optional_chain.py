"""An expression using ``?.`` or ``?[``."""
from typing import Any
from ._base import TypyExpression

class OptionalChain(TypyExpression):
    """``base`` followed by ``links`` (a list of ``ChainLink``), at least one
    of which is guarded (spec §24). Chains with no guarded link are plain
    Python and never become this node."""
    _fields: tuple = ('base', 'links')

    def __init__(self: OptionalChain, base: Any=None, links: Any=None) -> None:
        self.base = base
        self.links = links if links is not None else []
