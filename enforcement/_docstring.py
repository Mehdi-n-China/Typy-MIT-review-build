"""Keeping a function's docstring first."""
from .. import tools
_PYAST: tools.types.ModuleType = tools.pyast

def split_docstring(body: list) -> tuple:
    """``(docstring_statements, rest)``: the leading docstring, if any, is
    split off so inserted statements go *after* it and ``__doc__`` survives.
    """
    if body and isinstance(body[0], _PYAST.Expr) and isinstance(body[0].value, _PYAST.Constant) and isinstance(body[0].value.value, str):
        return (body[:1], body[1:])
    return ([], body)
