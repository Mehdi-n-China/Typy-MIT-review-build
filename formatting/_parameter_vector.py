"""An ordered group of parameters."""
from typing import Any

class ParameterVector:
    """An ordered list of ``Parameter`` nodes that knows how to print itself.

    Vectors and parameters combine with ``+``::

        ParameterVector([a]) + b        # a vector holding a, b
        ParameterVector([a]) + vector   # concatenation
    """

    def __init__(self: ParameterVector, parameters: Any=None) -> None:
        self.parameters = list(parameters or [])

    def __add__(self: ParameterVector, other: Any) -> Any:
        if isinstance(other, ParameterVector):
            return ParameterVector(self.parameters + other.parameters)
        if hasattr(other, 'formatted'):
            return ParameterVector(self.parameters + [other])
        return NotImplemented

    def __iter__(self: ParameterVector) -> Any:
        return iter(self.parameters)

    def __len__(self: ParameterVector) -> int:
        return len(self.parameters)

    @property
    def formatted(self: ParameterVector) -> str:
        """The Python-side parameter list: ``a: int, /, b: str = 'x'``."""
        return ', '.join((parameter.formatted for parameter in self.parameters))
