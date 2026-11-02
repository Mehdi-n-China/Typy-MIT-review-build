"""Delimiter matching over token lists."""
from typing import Any
from .. import tools
from ..errors import TypySyntaxError
_PAIRS: dict = {'(': ')', '[': ']', '{': '}'}
_CLOSERS: frozenset = frozenset(_PAIRS.values())

def find_closing_bracket(tokens: list, open_index: int, filename: str='<typy>') -> int:
    """Index of the bracket that closes the one at ``tokens[open_index]``.

    A mismatched or missing closer raises ``TypySyntaxError`` that names the
    delimiter the user forgot.
    """
    stack: list = []
    for index in range(open_index, len(tokens)):
        token: tools.tokens.TokenInfo = tokens[index]
        if token.type != tools.tokens.OP:
            continue
        if token.string in _PAIRS:
            stack.append(token)
        elif token.string in _CLOSERS:
            if not stack or _PAIRS[stack[-1].string] != token.string:
                opener: Any = stack[-1].string if stack else None
                detail: str = f'expected \'{_PAIRS[opener]}\'' if opener else 'no matching opening delimiter'
                raise TypySyntaxError(f'unmatched \'{token.string}\': {detail}', token.start[0], token.start[1], filename)
            stack.pop()
            if not stack:
                return index
    opener = tokens[open_index]
    raise TypySyntaxError(f'\'{opener.string}\' was never closed', opener.start[0], opener.start[1], filename)

def split_top_level(tokens: list, separator: str=',') -> list:
    """Split ``tokens`` on ``separator`` tokens that sit outside any brackets.

    Returns a list of token lists. An empty input gives an empty list; a
    trailing separator does not add an empty final group.
    """
    groups: list = []
    group: list = []
    depth: int = 0
    for token in tokens:
        if token.type == tools.tokens.OP:
            if token.string in _PAIRS:
                depth += 1
            elif token.string in _CLOSERS:
                depth -= 1
            elif token.string == separator and depth == 0:
                groups.append(group)
                group = []
                continue
        group.append(token)
    if group:
        groups.append(group)
    return groups
