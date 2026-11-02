"""Resolving a function: its parameters, its body, its own scope."""
from .. import tools
from ..tree import FunctionDeclaration, ParameterKind
from ._binding_for_type import binding_for_type
from ._collect_names import collect_names
from ._scope import Scope
from ._binding import Binding
from ..context import CompileContext
from ._diagnostics import Diagnostics

def resolve_function(function: FunctionDeclaration, scope: Scope, ctx: CompileContext, diagnostics: Diagnostics, resolve_block: tools.types.FunctionType) -> None:
    """Open a scope for ``function``, seed it with its typed parameters and
    resolve the body. ``resolve_block`` is passed in to avoid an import cycle.

    Parameters are declarations: each one is bound with the kind its type
    implies, so reassigning a parameter inside the body is checked just like
    reassigning any other typed variable.
    """
    inner: Scope = Scope('function', scope)
    function.scope = inner
    for parameter in function.signature.parameters:
        if parameter.kind in (ParameterKind.SLASH, ParameterKind.STAR):
            continue
        binding: Binding = binding_for_type(parameter.type, ctx)
        parameter.binding = binding
        inner.known.add(parameter.name)
        inner.current[parameter.name] = binding
    collect_names(function.body, inner)
    resolve_block(function.body, inner, ctx, diagnostics)
