"""Turning a ``TypeRef`` into the Python annotation it stands for."""
from typing import Any
from .. import tools
from ..context import CompileContext
_PYAST: tools.types.ModuleType = tools.pyast

def annotation_for(type_ref: Any, ctx: CompileContext) -> Any:
    """The annotation expression for ``type_ref``.

    ``any`` and ``dyn`` are not real Python types (and ``any`` collides with a
    builtin), so both become ``typing.Any``; ``void`` has no Python spelling
    and becomes ``None``. Everything else is its own dotted name.
    """
    if type_ref is None:
        return None
    if type_ref.is_any or type_ref.is_dyn:
        ctx.uses_any = True
        return _PYAST.Name(id='Any', ctx=_PYAST.Load())
    if type_ref.is_void:
        return _PYAST.Constant(value=None)
    return type_ref.to_expression()
