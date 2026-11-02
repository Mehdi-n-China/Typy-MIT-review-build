"""Recognising literals in the syntax tree."""
from typing import Any
from .. import tools
_CONSTANT_NAMES: dict = {type(None): 'None', bool: 'bool', int: 'int', float: 'float', str: 'str', bytes: 'bytes', complex: 'complex', type(Ellipsis): 'Ellipsis'}
_DISPLAYS: dict = {tools.pyast.List: 'list', tools.pyast.Tuple: 'tuple', tools.pyast.Set: 'set', tools.pyast.Dict: 'dict'}
_NUMERIC: set = {'int', 'float', 'complex'}

def literal_type_of(node: Any) -> Any:
    """The literal category of ``node`` (``"int"``, ``"str"``...) or ``None``.

    Only expressions that are *directly* a literal count (spec §8-9): a
    constant, a list/tuple/set/dict display, a negated number such as ``-5``,
    or a complex literal written ``real +/- imaginary`` such as ``3+4j``.
    Anything else, however obvious (``1 + 2``, ``len(x)``), is an arbitrary
    expression that Typy deliberately trusts.

    Matching is by exact type, so ``True`` is a ``bool`` and never an ``int``.
    """
    if isinstance(node, tools.pyast.Constant):
        return _CONSTANT_NAMES.get(type(node.value))
    for display, name in _DISPLAYS.items():
        if isinstance(node, display):
            return name
    if isinstance(node, tools.pyast.UnaryOp) and isinstance(node.op, tools.pyast.USub):
        inner: Any = literal_type_of(node.operand)
        return inner if inner in _NUMERIC else None
    if isinstance(node, tools.pyast.BinOp) and isinstance(node.op, (tools.pyast.Add, tools.pyast.Sub)):
        left: Any = None
        right: Any = None
        left, right = (literal_type_of(node.left), literal_type_of(node.right))
        if left in _NUMERIC and right in _NUMERIC and ('complex' in (left, right)):
            return 'complex'
    return None
