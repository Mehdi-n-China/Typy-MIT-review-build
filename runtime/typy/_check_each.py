"""Checking the elements collected by ``*type name`` / ``**type name``."""
from typing import Any
from ._errors import TypyTypeError
from ._monitor_hook import report

def check_each(values: Any, expected_type: type, name: str) -> None:
    """Check every element of ``values`` against ``expected_type`` exactly."""
    for position, value in enumerate(values):
        actual: type = type(value)
        ok: bool = actual is expected_type
        report('each', f'{name}[{position}]', expected_type, actual, ok)
        if not ok:
            raise TypyTypeError(f'{name}[{position}]: expected {expected_type.__name__}, got {actual.__name__}')
