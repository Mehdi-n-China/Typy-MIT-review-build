"""``Program`` -> ``ast.Module``."""
from .. import tools
from ._walk import lower_list
from ..context import CompileContext
from ..tree import Program

def lower_program(program: Program, ctx: CompileContext) -> tools.pyast.Module:
    """The whole file as a plain Python module."""
    return tools.pyast.Module(body=lower_list(program.body, ctx), type_ignores=[])
