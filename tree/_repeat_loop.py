"""``repeat N:``."""
from typing import Any
from ._base import TypyStatement

class RepeatLoop(TypyStatement):
    """``repeat count:`` runs its body ``count`` times with no user-visible
    iteration variable (spec §21); it lowers to ``for __ in range(count):``."""
    _fields: tuple = ('count', 'body', 'orelse')

    def __init__(self: RepeatLoop, count: Any=None, body: Any=None, orelse: Any=None) -> None:
        self.count = count
        self.body = body if body is not None else []
        self.orelse = orelse if orelse is not None else []
