"""The expressions a statement evaluates itself."""
from typing import Any
from .. import tools
from ..tree import Branch
_PYAST: tools.types.ModuleType = tools.pyast
_CLAUSES: tuple = (_PYAST.ExceptHandler, _PYAST.match_case, Branch)

def expression_roots(statement: Any) -> tools.types.GeneratorType:
    """The parts of ``statement`` that are expressions evaluated by the
    statement itself, excluding nested statement blocks (a conditional's
    branch tests are included, its branch bodies are not)."""
    for child in _PYAST.iter_child_nodes(statement):
        if isinstance(child, _PYAST.stmt):
            continue
        if isinstance(child, _CLAUSES):
            for part in _PYAST.iter_child_nodes(child):
                if not isinstance(part, _PYAST.stmt):
                    yield part
        else:
            yield child

def is_statement_call(parent: Any, grandparent: Any) -> bool:
    """A call is a harmless standalone statement when it *is* the expression
    statement, or is awaited directly as one (``await task()``)."""
    if isinstance(parent, _PYAST.Expr):
        return True
    return isinstance(parent, _PYAST.Await) and isinstance(grandparent, _PYAST.Expr)
