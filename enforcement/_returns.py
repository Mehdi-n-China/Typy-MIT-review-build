"""Enforcing declared return types."""
from typing import Any
from .. import tools
from ._calls import runtime_call, runtime_type_expression
from ._contains_yield import walk_function_body
from ..context import CompileContext
from ..tree import FunctionDeclaration, TypeRef
_PYAST: tools.types.ModuleType = tools.pyast

def enforce_returns(function: FunctionDeclaration, body: list, ctx: CompileContext) -> list:
    """Check every value ``function`` returns against its declared type.

    Each ``return value`` becomes ``return typy.check(value, T, 'f() return')``
    and, when the function can run off its end (which returns ``None``), a
    final checked ``return`` is appended, so a missing return is caught too.
    ``any`` / ``dyn`` / ``void`` return types and generators are left alone.
    """
    returns: TypeRef = function.signature.returns
    if returns.is_pseudo or any((isinstance(n, (_PYAST.Yield, _PYAST.YieldFrom)) for n in walk_function_body(body))):
        return body
    label: _PYAST.Constant = _PYAST.Constant(value=f'{function.name}() return')

    def check(value: Any) -> _PYAST.Call:
        return runtime_call(ctx, 'check', [value, runtime_type_expression(returns), label])
    for node in walk_function_body(body):
        if isinstance(node, _PYAST.Return):
            if node.value is None and returns.is_none:
                continue
            node.value = check(node.value if node.value is not None else _PYAST.Constant(value=None))
    if returns.is_none or (body and isinstance(body[-1], (_PYAST.Return, _PYAST.Raise))):
        return body
    return body + [_PYAST.Return(value=check(_PYAST.Constant(value=None)))]
