"""``i(0) while ...:`` and ``i(0) until ...:``."""
from typing import Any
from ._base import TypyStatement

class InitializedLoop(TypyStatement):
    """A loop that owns throwaway variables (spec §17-18).

    ``bindings`` is a list of ``LoopBinding``; ``mode`` is ``"while"`` or
    ``"until"``. The variables are created before the first test and deleted
    when the loop ends, however it ends (normally, ``break`` or an
    exception), so lowering wraps the loop in ``try`` / ``finally``.
    """
    _fields: tuple = ('bindings', 'mode', 'test', 'body', 'orelse')

    def __init__(self: InitializedLoop, bindings: Any=None, mode: str='while', test: Any=None, body: Any=None, orelse: Any=None) -> None:
        self.bindings = bindings if bindings is not None else []
        self.mode = mode
        self.test = test
        self.body = body if body is not None else []
        self.orelse = orelse if orelse is not None else []
