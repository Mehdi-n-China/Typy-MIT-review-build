"""Printing the lowered tree."""
from typing import Any
from .. import tools
_PYAST: tools.types.ModuleType = tools.pyast
_BLOCKS: tuple = (_PYAST.FunctionDef, _PYAST.AsyncFunctionDef, _PYAST.ClassDef)

def unparse_with_spacing(statements: list) -> str:
    """``ast.unparse`` each top-level statement and join them with a blank
    line wherever a function or class is involved; the whole-module
    ``unparse`` does not separate top-level definitions on its own."""
    pieces: list = []
    previous: Any = None
    for position, statement in enumerate(statements):
        if previous is not None and (isinstance(previous, _BLOCKS) or isinstance(statement, _BLOCKS)):
            pieces.append('')
        printable: Any = statement
        if position == 0:
            printable = _PYAST.Module(body=[statement], type_ignores=[])
        pieces.append(_PYAST.unparse(printable))
        previous = statement
    return '\n'.join(pieces) + '\n'
