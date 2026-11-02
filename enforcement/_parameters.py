"""Enforcing parameter types at function entry."""
from typing import Any
from .. import tools
from ..semantics import BindingKind
from ..tree import FunctionDeclaration, ParameterKind
from ._any_state import any_state_statement
from ._calls import runtime_call, runtime_type_expression
from ._checked_value import checked_value
from ..context import CompileContext
_PYAST: tools.types.ModuleType = tools.pyast

def parameter_prologue(function: FunctionDeclaration, ctx: CompileContext) -> list:
    """Statements that run first in ``function`` and check each argument.

    A normal parameter is re-bound to its checked value; ``*type name`` and
    ``**type name`` check every element they collected. ``any`` parameters
    establish their type from the value actually passed in.
    """
    statements: list = []
    for parameter in function.signature.parameters:
        binding: Any = getattr(parameter, 'binding', None)
        if binding is None or binding.kind not in (BindingKind.CONCRETE, BindingKind.ANY):
            continue
        name: _PYAST.Name = _PYAST.Name(id=parameter.name, ctx=_PYAST.Load())
        label: _PYAST.Constant = _PYAST.Constant(value=parameter.name)
        if parameter.kind == ParameterKind.NORMAL:
            if binding.kind == BindingKind.ANY:
                statements.append(any_state_statement(binding, ctx))
            statements.append(_PYAST.Assign(targets=[_PYAST.Name(id=parameter.name, ctx=_PYAST.Store())], value=checked_value(name, binding, parameter.name, ctx)))
        elif binding.kind == BindingKind.CONCRETE:
            values: Any = name
            if parameter.kind == ParameterKind.KWARG:
                values = _PYAST.Call(func=_PYAST.Attribute(value=name, attr='values', ctx=_PYAST.Load()), args=[], keywords=[])
            statements.append(_PYAST.Expr(value=runtime_call(ctx, 'check_each', [values, runtime_type_expression(parameter.type), label])))
    return statements
