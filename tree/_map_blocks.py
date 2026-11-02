"""Rewriting the statement blocks of a compound statement in place."""
from typing import Any
from .. import tools
from ._branch import Branch
_CLAUSES: tuple = (tools.pyast.ExceptHandler, tools.pyast.match_case, Branch)

def map_blocks(node: Any, function: Any) -> None:
    """Replace every statement block nested directly in ``node`` with
    ``function(block)``.

    The counterpart of ``child_blocks`` for passes that rewrite statements:
    a block is a list-of-statements field, and the blocks owned by clauses
    (``except`` handlers, ``match`` cases, conditional branches) are rewritten
    through the clause's ``body``.
    """
    for name in node._fields:
        value: Any = getattr(node, name, None)
        if not isinstance(value, list) or not value:
            continue
        head: Any = value[0]
        if isinstance(head, tools.pyast.stmt):
            setattr(node, name, function(value))
        elif isinstance(head, _CLAUSES):
            for clause in value:
                clause.body = function(clause.body)
