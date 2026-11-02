"""A helpful error for a typed declaration that forgot its value."""
from typing import Any
from .. import tools
from ..errors import TypySyntaxError
from ..lexer import read_dotted_name
from ..reserved import PY_HARD_KEYWORDS
from ._context import ParseContext

def reject_declaration_without_value(ctx: ParseContext, tokens: list) -> None:
    """Turn a bare ``int x`` into a helpful error instead of Python's generic
    "invalid syntax": a typed declaration always needs ``= value``."""
    parsed: Any = read_dotted_name(tokens, 0)
    if parsed is None:
        return
    after_type: Any = None
    parts: Any = None
    after_type, parts = parsed
    if after_type == len(tokens) - 1:
        name: tools.tokens.TokenInfo = tokens[after_type]
        if name.type == tools.tokens.NAME and name.string not in PY_HARD_KEYWORDS:
            raise TypySyntaxError(f"a typed declaration needs a value: '{'.'.join(parts)} {name.string}'", name.start[0], name.start[1], ctx.filename, hint=f"write e.g. '{'.'.join(parts)} {name.string} = ...'")
