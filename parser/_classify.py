"""Deciding what kind of statement a logical line starts."""
from .. import tools
from ._function import match_function_declaration
from ._initialized_loop import match_initialized_loop
from ..lexer import LogicalLine
_COMPOUND: dict = {'if': 'if', 'unless': 'if', 'while': 'while', 'for': 'for', 'try': 'try', 'with': 'with', 'class': 'class', 'def': 'def', 'until': 'until', 'forever': 'forever', 'repeat': 'repeat', 'match': 'match'}
_ORPHANS: frozenset = frozenset({'elif', 'elunless', 'else', 'except', 'finally'})

def classify_line(line: LogicalLine) -> str:
    """Name the kind of statement ``line`` begins (a key of ``PARSERS``).

    The first token decides almost everything. Only two Typy forms have to be
    recognised by shape because they begin with ordinary names: the
    initialized loop (``i(0) while ...``) and the typed function signature
    (``int f(...):``).
    """
    tokens: list = line.tokens
    first: tools.tokens.TokenInfo = tokens[0]
    if first.type == tools.tokens.OP:
        return 'decorator' if first.string == '@' else 'simple'
    if first.type != tools.tokens.NAME:
        return 'simple'
    word: str = first.string
    if word == 'async' and len(tokens) > 1:
        if tokens[1].string in ('for', 'with'):
            return tokens[1].string
        if tokens[1].string == 'def':
            return 'def'
        return 'function' if match_function_declaration(tokens) else 'simple'
    if word in _ORPHANS:
        return 'orphan'
    if word == 'case' and tokens[-1].string == ':':
        return 'orphan'
    if word in _COMPOUND:
        return _COMPOUND[word]
    if match_initialized_loop(tokens):
        return 'initialized_loop'
    if match_function_declaration(tokens):
        return 'function'
    return 'simple'
