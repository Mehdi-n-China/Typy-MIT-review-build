"""Reading (possibly dotted) type names such as ``int`` or ``Parent.Car``."""
from typing import Any
from .. import tools
from ..reserved import PY_HARD_KEYWORDS
_NOT_TYPE_NAMES: frozenset = PY_HARD_KEYWORDS - {'None'}

def read_dotted_name(tokens: list, start: int) -> Any:
    """Parse ``NAME (. NAME)*`` starting at ``tokens[start]``.

    Returns ``(end_index, parts)`` where ``end_index`` is the index just past
    the name and ``parts`` is the list of dotted segments, or ``None`` if
    there is no usable name at ``start``. Python's hard keywords never count
    (``return Car()`` is not a type), with one exception: ``None`` is a real
    Typy type for both variables and return values.
    """
    if start >= len(tokens):
        return None
    first: tools.tokens.TokenInfo = tokens[start]
    if first.type != tools.tokens.NAME or first.string in _NOT_TYPE_NAMES:
        return None
    if first.string == 'None':
        return (start + 1, ['None'])
    parts: list = [first.string]
    index: int = start + 1
    while index + 1 < len(tokens) and tokens[index].type == tools.tokens.OP and (tokens[index].string == '.') and (tokens[index + 1].type == tools.tokens.NAME) and (tokens[index + 1].string not in PY_HARD_KEYWORDS):
        parts.append(tokens[index + 1].string)
        index += 2
    return (index, parts)
