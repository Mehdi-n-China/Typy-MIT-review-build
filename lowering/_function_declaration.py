"""``FunctionDeclaration`` -> ``def`` / ``async def``."""
from typing import Any
from .. import tools
from ._annotation import annotation_for
from ._arguments import build_arguments
from ._walk import lower_list, lower_node
from ..context import CompileContext
_PYAST: tools.types.ModuleType = tools.pyast

def lower_function_declaration(node: Any, ctx: CompileContext) -> list:
    """``int add(int a, int b):`` becomes ``def add(a: int, b: int) -> int:``.

    ``void`` lowers to ``-> None`` (Python has no void; the difference from a
    ``None`` function exists only at compile time) and ``any`` / ``dyn`` to
    ``typing.Any``.
    """
    function_type: Any = _PYAST.AsyncFunctionDef if node.is_async else _PYAST.FunctionDef
    lowered: Any = function_type(name=node.name, args=build_arguments(node.signature.parameters, ctx), body=lower_list(node.body, ctx) or [_PYAST.Pass()], decorator_list=[lower_node(decorator, ctx) for decorator in node.decorators], returns=annotation_for(node.signature.returns, ctx), type_comment=None)
    if 'type_params' in function_type._fields:
        lowered.type_params = []
    return [_PYAST.copy_location(lowered, node)]
