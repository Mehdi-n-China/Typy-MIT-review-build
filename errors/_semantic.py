"""Compile-time rule violations."""
from ._base import TypyBaseError

class TypySemanticError(TypyBaseError):
    """The program parses, but breaks a rule Typy can verify at compile time."""

class TypyReservedIdentifierError(TypySemanticError):
    """A reserved word (``any``, ``void``, ``__``, ...) was used as a name."""
