"""A ``void`` function's result may never be used as a value (spec §13)."""
from typing import Any
from ..tree import child_blocks, Program
from ._expression_roots import expression_roots
from ._void_scan import scan_for_void_calls
from ._diagnostics import Diagnostics
from ._scope import Scope

def _check_statements(statements: list, scope: Scope, diagnostics: Diagnostics) -> None:
    for statement in statements:
        for root in expression_roots(statement):
            scan_for_void_calls(root, statement, None, scope, diagnostics)
        inner: Any = getattr(statement, 'scope', scope)
        for block in child_blocks(statement):
            _check_statements(block, inner, diagnostics)

def check_void_misuse(program: Program, diagnostics: Diagnostics) -> None:
    """Report calls to ``void`` functions whose result is used as a value
    (assigned, passed along, returned, printed...). Only functions declared in
    the file being compiled are known: the compiler sees one file at a time."""
    _check_statements(program.body, program.scope, diagnostics)
