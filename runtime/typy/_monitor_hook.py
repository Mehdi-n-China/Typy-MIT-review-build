"""The single hook the enforcement monitor attaches to."""
from typing import Any
_monitor: Any = None

def set_monitor(callback: Any) -> None:
    """Install ``callback`` (or ``None`` to remove it). It receives one dict
    per check: ``kind`` (``concrete`` / ``any`` / ``each``), ``name``,
    ``expected`` (a type, or ``None`` for an ``any`` still unestablished),
    ``actual`` (the value's type) and ``ok``.

    Every compiled file shares one runtime module, so installing the hook
    once is enough to observe the whole program.
    """
    global _monitor
    _monitor = callback

def report(kind: str, name: str, expected: Any, actual: type, ok: bool) -> None:
    """Tell the monitor about a check. A broken monitor must never take down
    the program it is watching, so its exceptions are swallowed."""
    if _monitor is not None:
        try:
            _monitor({'kind': kind, 'name': name, 'expected': expected, 'actual': actual, 'ok': ok})
        except Exception:
            pass
