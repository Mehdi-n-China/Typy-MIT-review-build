"""The text of one source file plus the means to slice it by token position."""
from typing import Any
from .. import tools

class SourceText:
    """Normalised source text with a line-offset table.

    Tokens report positions as ``(line, column)``; this class turns them into
    absolute offsets so the parser can cut exact slices of the original text
    (comments and odd spacing included) and hand them to Python's parser.
    """

    def __init__(self: SourceText, text: str, filename: str='<typy>') -> None:
        self.text = text
        self.filename = filename
        starts: list = [0]
        for line in text.split('\n'):
            starts.append(starts[-1] + len(line) + 1)
        self._line_starts = starts

    def offset(self: SourceText, line: int, col: int) -> int:
        """Absolute offset of 1-based ``line``, 0-based ``col``."""
        return self._line_starts[line - 1] + col

    def slice(self: SourceText, first: tools.tokens.TokenInfo, last: Any) -> str:
        """Source text from the start of token ``first`` to the end of ``last``."""
        return self.text[self.offset(*first.start):self.offset(*last.end)]
