"""Bugs in Typy itself."""
from ._base import TypyBaseError

class TypyInternalError(TypyBaseError):
    """A bug in Typy itself rather than in the program being compiled."""
