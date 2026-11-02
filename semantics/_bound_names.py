"""Which names a target or a pattern binds."""
from typing import Any
from .. import tools
_PYAST: tools.types.ModuleType = tools.pyast

def target_names(target: Any) -> tools.types.GeneratorType:
    """Names bound by an assignment-style target (``a``, ``a, (b, c)``, ``*a``)."""
    if isinstance(target, _PYAST.Name):
        yield target.id
    elif isinstance(target, (_PYAST.Tuple, _PYAST.List)):
        for element in target.elts:
            yield from target_names(element)
    elif isinstance(target, _PYAST.Starred):
        yield from target_names(target.value)

def pattern_names(node: Any) -> tools.types.GeneratorType:
    """Capture names bound by a ``match`` pattern node."""
    if isinstance(node, (_PYAST.MatchAs, _PYAST.MatchStar)) and node.name:
        yield node.name
    elif isinstance(node, _PYAST.MatchMapping) and node.rest:
        yield node.rest
