"""State shared by every parsing function."""
from typing import Any
from ..lexer import SourceText

class ParseContext:
    """What the parser needs to know about the file it is reading: the
    ``SourceText`` (for slicing exact source text), the filename (for error
    messages) and every identifier seen in the file (so generated names can
    steer clear of them)."""

    def __init__(self: ParseContext, source: SourceText, names: Any) -> None:
        self.source = source
        self.filename = source.filename
        self.names = names
