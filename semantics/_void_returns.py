"""``void`` functions cannot return at all (spec §13)."""
from typing import Any
from .. import tools
from ..errors import TypyVoidError
from ..tree import FunctionDeclaration, is_scope_node, Program
from ._diagnostics import Diagnostics

def _returns_in(nodes: list) -> tools.types.GeneratorType:
    """Every ``return`` in ``nodes`` that belongs to the same function."""
    stack: list = list(nodes)
    while stack:
        node: Any = stack.pop()
        if isinstance(node, tools.pyast.Return):
            yield node
        elif not is_scope_node(node) and (not isinstance(node, tools.pyast.Lambda)):
            stack.extend(tools.pyast.iter_child_nodes(node))

def check_void_returns(program: Program, diagnostics: Diagnostics) -> None:
    """Report any ``return`` (even a bare one) inside a ``void`` function."""
    for node in tools.pyast.walk(program):
        if isinstance(node, FunctionDeclaration) and node.signature.returns.is_void:
            for statement in _returns_in(node.body):
                diagnostics.report(TypyVoidError, f'\'{node.name}\' is declared void and cannot contain a return statement', statement, hint="void functions produce no value at all; declare it 'None' if it should return None")
