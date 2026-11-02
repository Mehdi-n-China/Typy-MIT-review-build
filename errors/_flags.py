"""Incompatible command line flags."""
from typing import Any
from ._base import TypyBaseError

class TypyFlagConflict(TypyBaseError):
    """Two command line flags that may not be used together were combined."""

    def __init__(self: Any, flags: list) -> None:
        super().__init__(f"Typy does not support the following flags in the same compilation run: {', '.join(flags)}")
