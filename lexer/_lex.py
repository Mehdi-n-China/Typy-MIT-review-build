"""The lexer's entry point."""
from typing import Any
from .. import tools
from ..errors import TypySyntaxError
from ..reserved import CHAIN_GUARD
from ._group_lines import group_logical_lines
from ._normalize import normalize_source
from ._source_text import SourceText
from ._tabs import check_indentation
from ._tokenize import tokenize_source

class LexedSource:
    """Everything the parser needs: the text, its logical lines, and the set
    of every identifier that appears (so generated names can avoid them)."""

    def __init__(self: LexedSource, source: SourceText, lines: list, names: Any) -> None:
        self.source = source
        self.lines = lines
        self.names = names

def lex_source(raw: str, filename: str='<typy>') -> LexedSource:
    """Lex raw source text into a ``LexedSource``.

    Order matters: tokenize first (bad delimiters / indentation surface
    here), reject the compiler-internal marker name, group into logical
    lines, then enforce the no-tabs rule on the result.
    """
    source: SourceText = SourceText(normalize_source(raw), filename)
    tokens: list = tokenize_source(source)
    names: set = set()
    for token in tokens:
        if token.type == tools.tokens.NAME:
            names.add(token.string)
            if token.string == CHAIN_GUARD:
                raise TypySyntaxError(f'\'{CHAIN_GUARD}\' is reserved for the compiler', token.start[0], token.start[1], filename)
    lines: list = group_logical_lines(tokens, source)
    check_indentation(lines, source)
    return LexedSource(source, lines, names)
