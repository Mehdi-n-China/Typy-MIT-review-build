"""Grouping tokens into indentation-nested logical lines."""
from typing import Any
from .. import tools
from ..errors import TypyIndentationError
from ._logical_line import LogicalLine
from ._source_text import SourceText
_IGNORED: tuple = (tools.tokens.NL, tools.tokens.COMMENT, tools.tokens.ENCODING)

def group_logical_lines(tokens: list, source: SourceText) -> list:
    """Return the top-level logical lines; each line's ``children`` holds the
    indented block beneath it (recursively).

    Python's tokenizer already marks block boundaries with INDENT / DEDENT
    tokens, so this is a straight walk with a stack: an INDENT descends into
    the previous line's ``children``, a DEDENT climbs back out.
    """
    root: list = []
    block: Any = root
    stack: list = []
    current: list = []
    previous: Any = None
    for token in tokens:
        kind: Any = token.type
        if kind in _IGNORED:
            continue
        if kind == tools.tokens.NEWLINE:
            if current:
                previous = LogicalLine(current)
                block.append(previous)
                current = []
        elif kind == tools.tokens.INDENT:
            if previous is None:
                raise TypyIndentationError('unexpected indent', token.start[0], token.start[1], source.filename)
            stack.append(block)
            block = previous.children
        elif kind == tools.tokens.DEDENT:
            block = stack.pop()
        elif kind == tools.tokens.ENDMARKER:
            break
        else:
            current.append(token)
    if current:
        block.append(LogicalLine(current))
    return root
