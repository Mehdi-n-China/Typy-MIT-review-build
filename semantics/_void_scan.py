"""Finding void calls used as values inside one expression."""
from typing import Any
from .. import tools
from ..errors import TypyVoidError
from ._expression_roots import is_statement_call
from ._void_scope_lookup import refers_to_void
from ._diagnostics import Diagnostics
from ._scope import Scope
_PYAST: tools.types.ModuleType = tools.pyast

def scan_for_void_calls(node: Any, parent: Any, grandparent: Any, scope: Scope, diagnostics: Diagnostics) -> None:
    """Report every call to a ``void`` function under ``node`` whose result is
    used (anything but a bare call statement)."""
    if isinstance(node, _PYAST.Call) and isinstance(node.func, _PYAST.Name) and refers_to_void(scope, node.func.id) and (not is_statement_call(parent, grandparent)):
        diagnostics.report(TypyVoidError, f'\'{node.func.id}\' is declared void; its result cannot be used as a value', node, hint='call it as a statement on its own line')
    for child in _PYAST.iter_child_nodes(node):
        scan_for_void_calls(child, node, parent, scope, diagnostics)
