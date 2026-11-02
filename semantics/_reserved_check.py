"""Reserved identifiers may never be *defined* (spec §4)."""
from typing import Any
from .. import tools
from ..errors import TypyReservedIdentifierError
from ..reserved import RESERVED_TERMS
from ..tree import FunctionDeclaration, LoopBinding, Parameter, Program, TypedDeclaration
from ._diagnostics import Diagnostics
_PYAST: tools.types.ModuleType = tools.pyast
_HINTS: dict = {'__': "'__' is the compiler's own throwaway name (it drives 'repeat'); a single '_' is free to use", 'typy': "'typy' is how generated code refers to the runtime support module"}

def _defined_name(node: Any) -> Any:
    """The name ``node`` defines, or ``None`` if it defines none."""
    if isinstance(node, _PYAST.Name) and isinstance(node.ctx, _PYAST.Store):
        return node.id
    if isinstance(node, _PYAST.arg):
        return node.arg
    if isinstance(node, (TypedDeclaration, FunctionDeclaration, LoopBinding, _PYAST.ClassDef)):
        return node.name
    if isinstance(node, Parameter) and (not node.is_marker):
        return node.name
    if isinstance(node, (_PYAST.ExceptHandler, _PYAST.MatchAs, _PYAST.MatchStar)):
        return node.name
    if isinstance(node, _PYAST.alias):
        return node.asname or node.name.split('.')[0]
    return None

def check_reserved_names(program: Program, diagnostics: Diagnostics) -> None:
    """Report every place a reserved word is used as a defined name.

    Only definitions count: assignment targets, parameters, loop and
    ``with``/``except`` targets, function and class names, imports, walrus
    and ``match`` captures. Referencing a reserved word is fine, which is why
    Python's builtin ``any(...)`` keeps working.
    """
    for node in tools.pyast.walk(program):
        name: Any = _defined_name(node)
        if name in RESERVED_TERMS:
            diagnostics.report(TypyReservedIdentifierError, f'\'{name}\' is reserved and cannot be used as an identifier', node, hint=_HINTS.get(name))
