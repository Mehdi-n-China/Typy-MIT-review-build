"""The parser's entry point."""
from typing import Any
from ..lexer import lex_source, LexedSource
from ..tree import Program
from ._block import parse_block
from ._context import ParseContext

def parse_source(raw: Any, filename: str='<typy>') -> tuple:
    """Parse Typy source text into a Typy AST.

    Returns ``(program, names)``: the ``Program`` node and the set of every
    identifier that occurs in the file. Lexing and syntax problems raise
    ``TypySyntaxError`` / ``TypyIndentationError``; meaning (types, scopes,
    reserved words) is checked later by ``Typy.semantics``.
    """
    lexed: LexedSource = lex_source(raw, filename)
    ctx: ParseContext = ParseContext(lexed.source, lexed.names)
    return (Program(parse_block(ctx, lexed.lines), filename), lexed.names)
