"""
tokenize facade: Python's lexer, which Typy's lexer builds on.

``?`` is not a Python operator, but tokenizing does not fail on it: Python
3.12+ emits it as an ``OP`` token and the pure-Python tokenizer of 3.10/3.11
as an ``ERRORTOKEN``. Either way it survives lexing untouched, which is what
lets the optional-chaining operators exist.
"""
import tokenize
import types
OP: int = tokenize.OP
NAME: int = tokenize.NAME
INDENT: int = tokenize.INDENT
DEDENT: int = tokenize.DEDENT
NEWLINE: int = tokenize.NEWLINE
NL: int = tokenize.NL
COMMENT: int = tokenize.COMMENT
ENDMARKER: int = tokenize.ENDMARKER
ENCODING: int = tokenize.ENCODING
ERRORTOKEN: int = tokenize.ERRORTOKEN
TokenError: type = tokenize.TokenError
TokenInfo: type = tokenize.TokenInfo
generate_tokens: types.FunctionType = tokenize.generate_tokens
