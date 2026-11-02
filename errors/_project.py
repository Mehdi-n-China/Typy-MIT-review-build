"""Unusable build targets."""
from ._base import TypyBaseError

class TypyProjectError(TypyBaseError):
    """The build target is unusable: missing, wrong kind, no entry point..."""
