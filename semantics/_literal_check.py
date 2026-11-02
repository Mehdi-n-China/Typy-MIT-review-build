"""Compile-time literal/type mismatches (spec §8)."""
from typing import Any
from .. import tools
from ..errors import TypyTypeMismatchError
from ..tree import Parameter, Program, TypedDeclaration
from ._literal_type_of import literal_type_of
from ._literals import LITERAL_TYPES
from ._type_ref_from_annotation import type_ref_from_annotation
from ._diagnostics import Diagnostics

def _check(type_ref: Any, value: Any, owner: Any, label: str, diagnostics: Diagnostics) -> None:
    """Report ``owner`` if ``value`` is a literal of a different category than
    ``type_ref``. Non-literal values and non-literal types are trusted."""
    if type_ref is None or value is None or type_ref.text not in LITERAL_TYPES:
        return
    actual: Any = literal_type_of(value)
    if actual is not None and actual != type_ref.text:
        diagnostics.report(TypyTypeMismatchError, f'type mismatch: {label} is declared {type_ref.text} but its value is a {actual} literal', owner)

def check_literal_types(program: Program, diagnostics: Diagnostics) -> None:
    """Check typed declarations, annotated assignments and parameter defaults.

    Typy never tries to work out what an arbitrary expression produces
    (``int x = some_call()`` is accepted); it only compares a declared type
    with a value that is *directly* a literal.
    """
    for node in tools.pyast.walk(program):
        if isinstance(node, TypedDeclaration):
            _check(node.type, node.value, node, f'\'{node.name}\'', diagnostics)
        elif isinstance(node, tools.pyast.AnnAssign) and isinstance(node.target, tools.pyast.Name):
            _check(type_ref_from_annotation(node.annotation), node.value, node, f'\'{node.target.id}\'', diagnostics)
        elif isinstance(node, Parameter) and (not node.is_marker):
            _check(node.type, node.default, node, f'parameter \'{node.name}\'', diagnostics)
