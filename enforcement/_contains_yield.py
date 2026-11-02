"""Is a function body a generator?"""
from typing import Any
from .. import tools
from ..tree import is_scope_node
_PYAST: tools.types.ModuleType = tools.pyast

def walk_function_body(statements: list) -> tools.types.GeneratorType:
    """Yield every node of a function body that belongs to *that* function
    (nested functions, classes and lambdas are skipped)."""
    stack: list = list(statements)
    while stack:
        node: Any = stack.pop()
        yield node
        if not is_scope_node(node) and (not isinstance(node, _PYAST.Lambda)):
            stack.extend(_PYAST.iter_child_nodes(node))

def contains_yield(statements: list) -> bool:
    """True if the body contains ``yield`` / ``yield from``, i.e. calling the
    function produces a generator and ``return`` has different meaning."""
    return any((isinstance(node, (_PYAST.Yield, _PYAST.YieldFrom)) for node in walk_function_body(statements)))
