"""Building located parse errors."""
from typing import Any
from .. import tools
from ..errors import TypyIndentationError, TypySyntaxError
from ._context import ParseContext

def syntax_error(ctx: ParseContext, message: str, token: tools.tokens.TokenInfo, hint: Any=None) -> TypySyntaxError:
    """A ``TypySyntaxError`` pointing at ``token``."""
    return TypySyntaxError(message, token.start[0], token.start[1], ctx.filename, hint)

def indentation_error(ctx: ParseContext, message: str, token: tools.tokens.TokenInfo, hint: Any=None) -> TypyIndentationError:
    """A ``TypyIndentationError`` pointing at ``token``."""
    return TypyIndentationError(message, token.start[0], token.start[1], ctx.filename, hint)
