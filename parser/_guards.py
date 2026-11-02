"""Preparing the text of a snippet that may contain optional-chaining ``?``."""
from typing import Any
from .. import tools
from ..errors import TypyChainError
from ..reserved import CHAIN_GUARD
from ._context import ParseContext
from ..lexer import SourceText

def segment_text(ctx: ParseContext, tokens: list) -> str:
    """The exact source text spanned by ``tokens``, with every ``?`` swapped
    for a marker Python's parser can read.

    ``a?.b`` becomes ``a .__typyg__.b`` and ``a?[k]`` becomes
    ``a .__typyg__[k]``: an ordinary attribute access on a name the user can
    never write. The parser later recognises that marker attribute and
    rebuilds the real ``OptionalChain`` node (see ``_chains``). A ``?`` that
    is not glued directly to a following ``.`` or ``[`` guards nothing and is
    a syntax error (spec §24).
    """
    source: SourceText = ctx.source
    base: Any = source.offset(*tokens[0].start)
    text: Any = source.text[base:source.offset(*tokens[-1].end)]
    edits: list = []
    for index, token in enumerate(tokens):
        if token.string != '?' or token.type not in (tools.tokens.OP, tools.tokens.ERRORTOKEN):
            continue
        following: Any = tokens[index + 1] if index + 1 < len(tokens) else None
        if following is None or following.type != tools.tokens.OP or following.string not in ('.', '[') or (following.start != token.end):
            raise TypyChainError("invalid use of '?': it must be directly followed by '.' or '['", token.start[0], token.start[1], ctx.filename, hint="optional chaining is written ?. or ?[ ... ]; a trailing '?' guards nothing")
        edits.append((source.offset(*token.start) - base, source.offset(*token.end) - base))
    for start, end in reversed(edits):
        text = text[:start] + ' .' + CHAIN_GUARD + text[end:]
    return text
