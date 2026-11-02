"""Turning source text into Python tokens, with Typy-flavoured errors."""
from typing import Any
from .. import tools
from ..errors import TypyIndentationError, TypySyntaxError
from ._source_text import SourceText
TAB_MESSAGE: str = "Tabs are not allowed in typy! If you wish to use tabs for indentation, please use your IDE's tab transformation feature!"

def tokenize_source(source: SourceText) -> list:
    """Tokenize a ``SourceText`` and return the raw token list.

    Python's tokenizer reports unterminated brackets and strings and broken
    indentation by raising; those become ``TypySyntaxError`` /
    ``TypyIndentationError`` carrying a location.
    """
    reader: tools.types.BuiltinFunctionType = tools.io.StringIO(source.text).readline
    try:
        return list(tools.tokens.generate_tokens(reader))
    except tools.tokens.TokenError as error:
        message: Any = None
        position: Any = None
        message, position = (error.args[0], error.args[1] if len(error.args) > 1 else (None, None))
        raise TypySyntaxError(f'{message} (unmatched delimiter or unterminated string?)', position[0], position[1], source.filename) from None
    except IndentationError as error:
        message = TAB_MESSAGE if 'tab' in (error.msg or '').lower() else error.msg
        raise TypyIndentationError(message, error.lineno, error.offset, source.filename) from None
    except SyntaxError as error:
        raise TypySyntaxError(error.msg, error.lineno, error.offset, source.filename) from None
