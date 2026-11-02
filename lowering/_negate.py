"""Logical negation of an expression."""
from typing import Any
from .. import tools

def negate(expression: Any) -> tools.pyast.UnaryOp:
    """``not expression`` (the lowering of ``unless`` / ``elunless`` / ``until``)."""
    return tools.pyast.UnaryOp(op=tools.pyast.Not(), operand=expression)
