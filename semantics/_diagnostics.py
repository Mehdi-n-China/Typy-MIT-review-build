"""Collecting compile-time problems instead of stopping at the first one."""
from typing import Any
from ..errors import TypyCompilationError

class Diagnostics:
    """An ordered bag of errors for one file.

    Semantic checks keep going after the first problem so a user sees every
    mistake in one run; ``raise_if_any`` turns the collection into a single
    ``TypyCompilationError`` sorted by position.
    """

    def __init__(self: Diagnostics, filename: str) -> None:
        self.filename = filename
        self.errors = []

    def report(self: Diagnostics, error_type: Any, message: str, node: Any, hint: Any=None) -> None:
        """Create ``error_type(message)`` located at ``node`` and keep it."""
        self.errors.append(error_type(message, getattr(node, 'lineno', None), getattr(node, 'col_offset', None), self.filename, hint))

    def raise_if_any(self: Diagnostics) -> None:
        if self.errors:
            ordered: list = sorted(self.errors, key=lambda error: (error.line or 0, error.col or 0))
            raise TypyCompilationError(ordered)
