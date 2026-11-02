"""The compiler's public entry point."""
from typing import Any
from . import tools
from .errors import TypyBaseError, TypyCompilationError, TypyInternalError
from .logger import logger
from .pipeline import compile_to_python

class CompileResult:
    """Outcome of compiling one source file.

    On success ``python_code`` holds the generated Python and ``errors`` is
    empty; on failure ``errors`` lists every diagnostic and ``python_code`` is
    ``None``. ``needs_runtime`` says the output imports the runtime package
    (``--enforce`` checks); ``uses_any_typing`` that it imports ``typing.Any``;
    ``trace`` holds the per-stage notes shown by ``--veritasium``.
    """

    def __init__(self: CompileResult, python_code: Any=None, errors: Any=None, needs_runtime: bool=False, uses_any_typing: bool=False, trace: Any=None) -> None:
        self.python_code = python_code
        self.errors = list(errors or [])
        self.needs_runtime = needs_runtime
        self.uses_any_typing = uses_any_typing
        self.trace = list(trace or [])

    @property
    def ok(self: CompileResult) -> bool:
        return not self.errors and self.python_code is not None

def compile_source(source: Any, filename: str='<typy>', enforce: bool=False) -> CompileResult:
    """Compile Typy ``source``; never raises for problems in the source.

    Syntax and semantic errors come back inside the ``CompileResult`` so a
    caller compiling many files can report all of them together. A crash
    inside the compiler itself is logged and reported as a
    ``TypyInternalError`` rather than escaping as a raw traceback.
    """
    try:
        code: Any = None
        ctx: Any = None
        code, ctx = compile_to_python(source, filename, enforce)
    except TypyCompilationError as failure:
        return CompileResult(errors=failure.errors)
    except TypyBaseError as failure:
        return CompileResult(errors=[failure])
    except Exception as crash:
        logger.crash(tools.trace.format_exc())
        return CompileResult(errors=[TypyInternalError(f'internal compiler error: {crash!r}', filename=filename)])
    return CompileResult(code, [], ctx.needs_runtime, ctx.uses_any, ctx.trace)
