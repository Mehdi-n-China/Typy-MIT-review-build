"""The lowering traversal."""
from typing import Any
from ._children import lower_children
from ._registry import HANDLERS
from ..context import CompileContext

def lower_node(node: Any, ctx: CompileContext) -> Any:
    """Lower ``node``: a registered Typy node goes to its handler, anything
    else keeps its shape and has its children lowered."""
    handler: Any = HANDLERS.get(type(node))
    if handler is not None:
        return handler(node, ctx)
    return lower_children(node, ctx, lower_node)

def lower_list(nodes: list, ctx: CompileContext) -> list:
    """Lower a list of nodes, flattening statements that expand into several."""
    result: list = []
    for node in nodes:
        lowered: Any = lower_node(node, ctx)
        result.extend(lowered if isinstance(lowered, list) else [lowered])
    return result
