"""The "no tabs for indentation" rule (spec §29)."""
from .. import tools
from ..errors import TypyIndentationError
from ._tokenize import TAB_MESSAGE
from ._source_text import SourceText

def check_indentation(lines: list, source: SourceText) -> None:
    """Raise if any logical line (at any depth) is indented with a tab.

    Only leading whitespace counts: a tab inside a string or between tokens
    is none of the compiler's business.
    """
    for line in lines:
        first: tools.tokens.TokenInfo = line.first
        if '\t' in first.line[:first.start[1]]:
            raise TypyIndentationError(TAB_MESSAGE, first.start[0], 0, source.filename)
        check_indentation(line.children, source)
