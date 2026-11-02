"""Checking ``any`` bindings."""
from typing import Any
from ._any_state import AnyState, MISSING
from ._errors import TypyTypeError
from ._monitor_hook import report

def check_any(value: Any, state: AnyState, name: str) -> Any:
    """Establish or enforce the type of an ``any`` binding.

    The first value seen for ``state`` fixes the binding's type, whatever it
    turns out to be at runtime; every later value must match it exactly.
    """
    actual: type = type(value)
    if state.established is MISSING:
        state.established = actual
        report('any', name, None, actual, True)
        return value
    ok: bool = actual is state.established
    report('any', name, state.established, actual, ok)
    if not ok:
        raise TypyTypeError(f'{name}: established as {state.established.__name__}, got {actual.__name__}')
    return value
