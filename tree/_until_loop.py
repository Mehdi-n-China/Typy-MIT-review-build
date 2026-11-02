"""``until condition:``."""
from typing import Any
from ._base import TypyStatement

class UntilLoop(TypyStatement):
    """``until test:`` runs while ``test`` is false (spec §19); it lowers to
    ``while not test:``. An optional ``else`` block behaves as on ``while``."""
    _fields: tuple = ('test', 'body', 'orelse')

    def __init__(self: UntilLoop, test: Any=None, body: Any=None, orelse: Any=None) -> None:
        self.test = test
        self.body = body if body is not None else []
        self.orelse = orelse if orelse is not None else []
