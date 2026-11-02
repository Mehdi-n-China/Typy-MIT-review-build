"""Walking statements and enforcing each kind."""
from typing import Any
from .. import tools
from ..tree import FunctionDeclaration, TypedDeclaration, map_blocks
from ._assignment import enforce_assignment, enforce_augmented
from ._declaration import enforce_declaration
from ._function import enforce_function
from ..context import CompileContext
_PYAST: tools.types.ModuleType = tools.pyast

def enforce_statement(statement: Any, ctx: CompileContext) -> list:
    """Enforce one statement; returns the list of statements replacing it."""
    if isinstance(statement, (TypedDeclaration, _PYAST.AnnAssign)):
        return enforce_declaration(statement, ctx)
    if isinstance(statement, _PYAST.Assign):
        return enforce_assignment(statement, ctx)
    if isinstance(statement, _PYAST.AugAssign):
        return enforce_augmented(statement, ctx)
    if isinstance(statement, FunctionDeclaration):
        return enforce_function(statement, ctx, enforce_block)
    map_blocks(statement, lambda block: enforce_block(block, ctx))
    return [statement]

def enforce_block(statements: list, ctx: CompileContext) -> list:
    """Enforce a list of statements, in order."""
    result: list = []
    for statement in statements:
        result.extend(enforce_statement(statement, ctx))
    return result
