"""The one place Python's parser is invoked."""
from typing import Any
from .. import tools
from ._chains import build_optional_chains
from ._relocate import relocate
from ._syntax_errors import convert_python_error
from ._context import ParseContext

def parse_python_text(ctx: ParseContext, text: str, mode: str, first: tools.tokens.TokenInfo, stub_line: int=1, col_shift: int=0) -> Any:
    """Parse ``text`` with ``ast.parse`` and return a tree located in the file.

    ``first`` is the token the snippet starts at; ``stub_line`` / ``col_shift``
    say how the snippet was wrapped (see ``relocate``). Guarded chains are
    rebuilt into ``OptionalChain`` nodes before the tree is returned, and any
    Python syntax error comes back as a located Typy error.
    """
    try:
        tree: Any = tools.pyast.parse(text, mode=mode)
    except SyntaxError as error:
        raise convert_python_error(ctx, error, first, stub_line, col_shift) from None
    relocate(tree, first.start[0], first.start[1] + col_shift, stub_line)
    return build_optional_chains(tree, ctx.filename)
