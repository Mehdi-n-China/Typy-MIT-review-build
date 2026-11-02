"""Several diagnostics reported together."""
from typing import Any
from ._base import TypyBaseError

class TypyCompilationError(TypyBaseError):
    """Several diagnostics gathered from one file (or one whole build).

    Semantic checks keep going after the first problem so the user can fix
    everything in one pass; this class carries the full list in ``errors``.
    """

    def __init__(self: Any, errors: Any) -> None:
        self.errors = list(errors)
        count: int = len(self.errors)
        super().__init__(f"{count} compilation error{'s' if count != 1 else ''}")

    def __str__(self: Any) -> str:
        return '\n'.join((str(error) for error in self.errors)) or self.message
