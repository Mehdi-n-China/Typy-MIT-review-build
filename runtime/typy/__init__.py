"""
The Typy runtime (imported by compiled code as ``import _typy_runtime as typy``).

Public surface used by generated code:

    typy.check(value, type, name)            exact-type check of a declared name
    typy.check_any(value, state, name)       establish / enforce an ``any`` type
    typy.check_each(values, type, name)      per-element check for ``*`` / ``**``
    typy.AnyState()                          holds the type an ``any`` fixed
    typy.TypyTypeError                       what a failed check raises
    typy.set_monitor(callback)               observe every check (used by --gui)

Matching is always by *exact* type: ``type(value) is expected``. A ``bool`` is
not an ``int`` and a subclass does not satisfy its parent (spec §10).

Since: 1.0.0
"""
from ._any_state import AnyState
from ._bootstrap import start_monitor_if_configured
from ._check import check
from ._check_any import check_any
from ._check_each import check_each
from ._errors import TypyTypeError
from ._monitor_hook import set_monitor
start_monitor_if_configured(__name__)
