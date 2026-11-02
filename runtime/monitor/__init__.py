"""
The ``--gui`` enforcement monitor (shipped as ``_typy_monitor``).

A live, text-mode view of the checks the runtime performs: each check as it
happens, plus a summary when the program exits. It observes the *real*
enforcement through the runtime's hook; it never re-computes or alters a
check. A graphical front-end can plug into the same hook later.

Since: 1.5.0 (rewritten as a package in 2.3.0)
"""
from ._attach import attach
from ._monitor import EnforcementMonitor
