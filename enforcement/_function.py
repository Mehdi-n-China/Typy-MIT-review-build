"""Enforcing a typed function: its parameters, body and return values."""
from typing import Any
from .. import tools
from ._docstring import split_docstring
from ._parameters import parameter_prologue
from ._returns import enforce_returns
from ..context import CompileContext
from ..tree import FunctionDeclaration

def enforce_function(function: FunctionDeclaration, ctx: CompileContext, enforce_block: tools.types.FunctionType) -> list:
    """Enforce ``function`` in place and return ``[function]``.

    The body is enforced first (``enforce_block`` is passed in to avoid an
    import cycle), then returns are checked, then the parameter checks are
    inserted after the docstring so they run before anything else.
    """
    body: list = enforce_block(function.body, ctx)
    body = enforce_returns(function, body, ctx)
    docstring: Any = None
    rest: Any = None
    docstring, rest = split_docstring(body)
    function.body = docstring + parameter_prologue(function, ctx) + rest
    return [function]
