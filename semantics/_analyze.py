"""The semantic stage's entry point."""
from ._diagnostics import Diagnostics
from ._literal_check import check_literal_types
from ._reserved_check import check_reserved_names
from ._resolve_program import resolve_program
from ._void_misuse import check_void_misuse
from ._void_returns import check_void_returns
from ..context import CompileContext
from ..tree import Program

def analyze_program(program: Program, ctx: CompileContext) -> None:
    """Run every compile-time check on ``program``.

    The checks are independent and all of them run, so one compilation
    reports every problem it can find; if there are any, a single
    ``TypyCompilationError`` listing them (sorted by position) is raised.
    On success the tree is annotated with scope/binding information for the
    enforcement and lowering stages.
    """
    diagnostics: Diagnostics = Diagnostics(ctx.filename)
    check_reserved_names(program, diagnostics)
    resolve_program(program, ctx, diagnostics)
    check_literal_types(program, diagnostics)
    check_void_returns(program, diagnostics)
    check_void_misuse(program, diagnostics)
    diagnostics.raise_if_any()
