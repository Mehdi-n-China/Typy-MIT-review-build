"""``forever:``."""
from typing import Any
from ._base import TypyStatement

class ForeverLoop(TypyStatement):
    """``forever:`` is an intentional infinite loop (spec §20); it lowers to
    ``while True:``."""
    _fields: tuple = ('body', 'orelse')

    def __init__(self: ForeverLoop, body: Any=None, orelse: Any=None) -> None:
        self.body = body if body is not None else []
        self.orelse = orelse if orelse is not None else []
