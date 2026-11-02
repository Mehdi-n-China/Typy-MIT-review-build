"""An if / unless chain."""
from typing import Any
from ._base import TypyStatement

class Conditional(TypyStatement):
    """A whole ``if`` / ``unless`` chain with optional ``elif`` / ``elunless``
    branches and a final ``else``.

    Every if-chain parses to this node, so Python's ``elif`` and Typy's
    ``elunless`` mix freely (spec §23): each branch is lowered on its own.
    """
    _fields: tuple = ('branches', 'orelse')

    def __init__(self: Conditional, branches: Any=None, orelse: Any=None) -> None:
        self.branches = branches if branches is not None else []
        self.orelse = orelse if orelse is not None else []
