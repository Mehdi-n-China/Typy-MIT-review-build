"""Exact-type checking of declared names."""
from typing import Any
from ._errors import TypyTypeError
from ._monitor_hook import report

def check(value: Any, expected_type: type, name: str) -> Any:
    """Return ``value`` if its type is exactly ``expected_type``, else raise.

    Subclasses do not count: a ``bool`` never satisfies ``int`` (spec §10).
    """
    actual: type = type(value)
    ok: bool = actual is expected_type
    report('concrete', name, expected_type, actual, ok)
    if not ok:
        raise TypyTypeError(f'{name}: expected {expected_type.__name__}, got {actual.__name__}')
    return value
