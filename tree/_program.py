"""The root of a parsed Typy file."""
from typing import Any
from .. import tools

class Program(tools.pyast.mod):
    """A whole Typy source file: a list of statements plus its filename.

    Lowering turns this into an ordinary ``ast.Module``.
    """
    _fields: tuple = ('body', 'filename')

    def __init__(self: Program, body: Any=None, filename: str='<typy>') -> None:
        self.body = body if body is not None else []
        self.filename = filename
