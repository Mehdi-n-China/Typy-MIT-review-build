"""``TypedDeclaration`` -> annotated assignment."""
from typing import Any
from .. import tools
from ._annotation import annotation_for
from ._walk import lower_node
from ..context import CompileContext
_PYAST: tools.types.ModuleType = tools.pyast

def lower_typed_declaration(node: Any, ctx: CompileContext) -> list:
    """``int x = 10`` becomes ``x: int = 10`` (spec §27)."""
    lowered: _PYAST.AnnAssign = _PYAST.AnnAssign(target=_PYAST.Name(id=node.name, ctx=_PYAST.Store()), annotation=annotation_for(node.type, ctx), value=lower_node(node.value, ctx), simple=1)
    return [_PYAST.copy_location(lowered, node)]
