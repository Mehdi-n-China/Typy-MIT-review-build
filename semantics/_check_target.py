"""The "declare before you assign" rule (spec §7)."""
from typing import Any
from .. import tools
from ..errors import TypyUndeclaredVariableError
from ._diagnostics import Diagnostics
from ._scope import Scope
_PYAST: tools.types.ModuleType = tools.pyast

def check_assignment_target(target: Any, scope: Scope, diagnostics: Diagnostics) -> None:
    """Report every plain name in an assignment target that the scope has
    never declared with a type (or bound some other way).

    ``x = 10`` is not valid Typy unless ``x`` was first introduced by a
    typed declaration, a loop target, a parameter, and so on. Unpacking
    targets are checked name by name, so ``a, b = 1, 2`` cannot be used to
    sidestep the rule. Attribute and subscript targets bind no name.
    """
    if isinstance(target, _PYAST.Name):
        name: str = target.id
        if name in scope.known or name in scope.current or name in scope.outer:
            return
        diagnostics.report(TypyUndeclaredVariableError, f'\'{name}\' is not declared', target, hint=f'give it a type the first time, e.g. \'int {name} = ...\', or use \'dyn {name} = ...\'')
    elif isinstance(target, (_PYAST.Tuple, _PYAST.List)):
        for element in target.elts:
            check_assignment_target(element, scope, diagnostics)
    elif isinstance(target, _PYAST.Starred):
        check_assignment_target(target.value, scope, diagnostics)
