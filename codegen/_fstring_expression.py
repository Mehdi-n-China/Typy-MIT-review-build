"""Printing an expression that may itself contain f-strings."""
from typing import Any
from .. import tools
from ._fstring_placeholders import extract_fstrings, restore_fstrings

def expression_source(expression: Any, enclosing: tuple=()) -> str:
    """Source text of ``expression`` with every f-string inside it printed by
    ``render_fstring``, respecting the quotes of the ``enclosing`` f-strings.
    The node is copied first, so printing never changes the tree."""
    holder: tools.pyast.Expression = tools.pyast.Expression(body=tools.copying.deepcopy(expression))
    pairs: list = extract_fstrings(holder)
    return restore_fstrings(tools.pyast.unparse(holder.body), pairs, enclosing)
