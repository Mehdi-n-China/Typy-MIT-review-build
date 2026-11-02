"""``TYPE name(TYPE param, ...):`` plus its body."""
from typing import Any
from ._base import TypyStatement

class FunctionDeclaration(TypyStatement):
    """A function written with Typy's typed signature (spec §15).

    This replaces Python's ``def``, which is not valid Typy. ``signature`` is
    a ``Signature``; ``decorators`` is a list of expressions; ``is_async`` is
    true for ``async TYPE name(...)``. Lowers to ``def`` / ``async def`` with
    annotations.
    """
    _fields: tuple = ('name', 'signature', 'body', 'decorators', 'is_async')

    def __init__(self: FunctionDeclaration, name: Any=None, signature: Any=None, body: Any=None, decorators: Any=None, is_async: bool=False) -> None:
        self.name = name
        self.signature = signature
        self.body = body if body is not None else []
        self.decorators = decorators if decorators is not None else []
        self.is_async = is_async
