"""
The compilation pipeline.

    source text
        -> lexer / parser      Typy AST                  (Typy.parser)
        -> semantic analysis   checked, annotated AST    (Typy.semantics)
        -> enforcement         AST + runtime checks      (Typy.enforcement)   [--enforce]
        -> lowering            plain Python AST          (Typy.lowering)
        -> code generation     Python source text        (Typy.codegen)

Each stage is its own package; this function only wires them together.
"""
from typing import Any
from . import tools
from .codegen import generate_python
from .context import CompileContext
from .enforcement import inject_enforcement
from .formatting import Formatter
from .lowering import lower_program
from .parser import parse_source
from .semantics import analyze_program
from .tree import FunctionDeclaration

def compile_to_python(source: Any, filename: str='<typy>', enforce: bool=False) -> tuple:
    """Compile Typy source to Python source.

    Returns ``(python_code, ctx)`` where ``ctx`` says whether the output needs
    the runtime package. Raises ``TypySyntaxError`` / ``TypyIndentationError``
    for malformed source and ``TypyCompilationError`` (carrying every
    diagnostic) for semantic errors.
    """
    program: Any = None
    names: Any = None
    program, names = parse_source(source, filename)
    ctx: CompileContext = CompileContext(filename, enforce, names)
    ctx.note(f'parsed {len(program.body)} top-level statement(s), {sum((1 for _ in tools.pyast.walk(program)))} AST nodes')
    for node in tools.pyast.walk(program):
        if isinstance(node, FunctionDeclaration):
            ctx.note(f'function {Formatter.signature(node)}')
    analyze_program(program, ctx)
    ctx.note('semantic analysis passed')
    if enforce:
        inject_enforcement(program, ctx)
        ctx.note(f'enforcement: {ctx.runtime_calls} runtime check(s) generated')
    code: str = generate_python(lower_program(program, ctx), ctx)
    ctx.note(f'generated {len(code.splitlines())} line(s) of Python')
    return (code, ctx)
