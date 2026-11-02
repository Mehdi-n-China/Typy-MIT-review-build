"""Declaration and literal-type errors."""
from ._semantic import TypySemanticError

class TypyUndeclaredVariableError(TypySemanticError):
    """A name was assigned without ever being declared with a type."""

class TypyTypeMismatchError(TypySemanticError):
    """A literal value does not match the type it was declared with."""
