"""Lowering the children of a node that needs no special treatment."""
from typing import Any
from .. import tools
from ..context import CompileContext
_PYAST: tools.types.ModuleType = tools.pyast

def lower_children(node: Any, ctx: CompileContext, lower: tools.types.FunctionType) -> Any:
    """Lower every child of ``node`` in place using ``lower`` and return it.

    Statement handlers may expand one statement into several, so a list
    field is rebuilt with each result flattened into it. Single-node fields
    always hold expressions, which lower to exactly one node.
    """
    for name, value in _PYAST.iter_fields(node):
        if isinstance(value, list):
            rebuilt: list = []
            for item in value:
                if isinstance(item, _PYAST.AST):
                    result: Any = lower(item, ctx)
                    rebuilt.extend(result if isinstance(result, list) else [result])
                else:
                    rebuilt.append(item)
            setattr(node, name, rebuilt)
        elif isinstance(value, _PYAST.AST):
            setattr(node, name, lower(value, ctx))
    return node
