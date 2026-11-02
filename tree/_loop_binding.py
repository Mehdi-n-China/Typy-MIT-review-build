"""One ``name(initial)`` pair of an initialized loop."""
from typing import Any
from ._base import TypyNode

class LoopBinding(TypyNode):
    """The ``i(0)`` in ``i(0) while i < 10:`` — a loop variable and the
    expression it starts from. Loop variables are implicitly ``dyn``."""
    _fields: tuple = ('name', 'value')

    def __init__(self: LoopBinding, name: Any=None, value: Any=None) -> None:
        self.name = name
        self.value = value
