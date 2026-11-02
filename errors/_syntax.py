"""Errors about the shape of the source text."""
from ._base import TypyBaseError

class TypySyntaxError(TypyBaseError):
    """The source is not valid Typy (malformed statement, bad delimiters...)."""

class TypyIndentationError(TypyBaseError):
    """Indentation is invalid: tabs, a missing block, an unexpected indent."""
