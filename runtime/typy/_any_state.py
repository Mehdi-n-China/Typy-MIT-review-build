"""The memory of an ``any`` binding."""
MISSING: object = object()

class AnyState:
    """Holds the type an ``any`` binding established.

    One instance is created per ``any`` declaration (not per name), so two
    declarations never share state even when they reuse a name.
    """
    __slots__: tuple = ('established',)

    def __init__(self: AnyState) -> None:
        self.established = MISSING
