"""Generic helpers for walking the statement structure of a mixed tree."""
from typing import Any
from .. import tools
from ._branch import Branch
from ._function_declaration import FunctionDeclaration
_CLAUSES: tuple = (tools.pyast.ExceptHandler, tools.pyast.match_case, Branch)
_SCOPES: tuple = (tools.pyast.FunctionDef, tools.pyast.AsyncFunctionDef, tools.pyast.ClassDef, FunctionDeclaration)

def child_blocks(node: Any) -> tools.types.GeneratorType:
    """Yield each list of statements nested directly inside ``node``.

    Works for Python and Typy compound statements alike by inspecting
    ``_fields``: a list of statements is a block (``body``, ``orelse``,
    ``finalbody``...), and a list of clauses (``except`` handlers, ``match``
    cases, conditional branches) contributes each clause's ``body``.
    """
    for name in node._fields:
        value: Any = getattr(node, name, None)
        if not isinstance(value, list) or not value:
            continue
        head: Any = value[0]
        if isinstance(head, tools.pyast.stmt):
            yield value
        elif isinstance(head, _CLAUSES):
            for clause in value:
                yield clause.body

def is_scope_node(node: Any) -> bool:
    """True for nodes that open a new Python scope (functions and classes)."""
    return isinstance(node, _SCOPES)
