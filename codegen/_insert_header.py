"""Where the generated imports go."""
from typing import Any
from .. import tools
_PYAST: tools.types.ModuleType = tools.pyast

def insert_header(module: Any, header: list) -> None:
    """Insert ``header`` into ``module.body`` after the module docstring and
    any ``from __future__ import ...`` lines, which Python requires to come
    first."""
    body: list = module.body
    index: int = 0
    if body and isinstance(body[0], _PYAST.Expr) and isinstance(body[0].value, _PYAST.Constant) and isinstance(body[0].value.value, str):
        index = 1
    while index < len(body) and isinstance(body[index], _PYAST.ImportFrom) and (body[index].module == '__future__'):
        index += 1
    module.body = body[:index] + header + body[index:]
