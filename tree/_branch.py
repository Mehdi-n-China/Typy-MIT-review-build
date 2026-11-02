"""One branch of a conditional chain."""
from typing import Any
from ._base import TypyNode

class Branch(TypyNode):
    """``if`` / ``unless`` / ``elif`` / ``elunless`` plus its test and body.

    ``kind`` is the keyword as written. ``unless`` and ``elunless`` are just
    ``if not`` / ``elif not``, so ``negated`` tells lowering to wrap the test
    in ``not`` (spec §22-23).
    """
    _fields: tuple = ('kind', 'test', 'body')

    def __init__(self: Branch, kind: str='if', test: Any=None, body: Any=None) -> None:
        self.kind = kind
        self.test = test
        self.body = body if body is not None else []

    @property
    def negated(self: Branch) -> bool:
        return self.kind in ('unless', 'elunless')
