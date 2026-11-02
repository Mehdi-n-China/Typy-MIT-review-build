"""Hooking the monitor up to the runtime."""
from typing import Any
import atexit
from ._monitor import EnforcementMonitor

def attach(runtime: Any, entry_point: str) -> EnforcementMonitor:
    """Create a monitor, install it as ``runtime``'s hook and arrange for its
    summary to print at exit. Returns the monitor."""
    monitor: EnforcementMonitor = EnforcementMonitor(entry_point)
    monitor.start()
    runtime.set_monitor(monitor)
    atexit.register(monitor.finish)
    return monitor
