"""Small predicates over logical lines."""
from .. import tools
from ..lexer import LogicalLine

def starts_with(line: LogicalLine, word: str) -> bool:
    """True if the logical line begins with the name ``word``."""
    first: tools.tokens.TokenInfo = line.first
    return first.type == tools.tokens.NAME and first.string == word

def is_op(token: tools.tokens.TokenInfo, text: str) -> bool:
    """True if ``token`` is the operator ``text``."""
    return token.type == tools.tokens.OP and token.string == text
