"""Walking a scope's code without wandering into nested scopes."""
from typing import Any
from .. import tools
from ..tree import is_scope_node

def walk_same_scope(nodes: list) -> tools.types.GeneratorType:
    """Yield every node reachable from ``nodes`` that belongs to the *same*
    Python scope.

    Function and class definitions are yielded (their names are bound in this
    scope) but never entered, and neither are lambdas, whose parameters live in a
    scope of their own.
    """
    stack: list = list(reversed(nodes))
    while stack:
        node: Any = stack.pop()
        yield node
        if is_scope_node(node) or isinstance(node, tools.pyast.Lambda):
            continue
        stack.extend(reversed(list(tools.pyast.iter_child_nodes(node))))
