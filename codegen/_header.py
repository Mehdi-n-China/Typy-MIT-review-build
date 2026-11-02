"""The import statements generated code needs."""
from .. import tools
from ..context import CompileContext
from ..reserved import RUNTIME_ALIAS, RUNTIME_MODULE
_PYAST: tools.types.ModuleType = tools.pyast

def build_header(ctx: CompileContext) -> list:
    """``from typing import Any`` if any annotation uses it, and
    ``import _typy_runtime as typy`` if any runtime check was generated."""
    header: list = []
    if ctx.uses_any:
        header.append(_PYAST.ImportFrom(module='typing', names=[_PYAST.alias(name='Any', asname=None)], level=0))
    if ctx.needs_runtime:
        header.append(_PYAST.Import(names=[_PYAST.alias(name=RUNTIME_MODULE, asname=RUNTIME_ALIAS)]))
    return header
