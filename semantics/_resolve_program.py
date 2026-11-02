"""Scope resolution for a whole file."""
from ._collect_names import collect_names
from ._resolve_statement import resolve_block
from ._scope import Scope
from ..context import CompileContext
from ._diagnostics import Diagnostics
from ..tree import Program

def resolve_program(program: Program, ctx: CompileContext, diagnostics: Diagnostics) -> None:
    """Build the module scope, resolve every statement and store the module
    scope on ``program.scope``."""
    scope: Scope = Scope('module')
    program.scope = scope
    collect_names(program.body, scope)
    resolve_block(program.body, scope, ctx, diagnostics)
