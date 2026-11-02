"""Statements that are never valid where they appear."""
from .. import tools
from ._errors import syntax_error
from ._context import ParseContext
_ORPHAN_MESSAGES: dict = {'elif': "'elif' without a matching 'if'", 'elunless': "'elunless' without a matching 'if' or 'unless'", 'else': "'else' without a matching 'if', 'unless', loop or 'try'", 'except': "'except' without a matching 'try'", 'finally': "'finally' without a matching 'try'", 'case': "'case' outside a 'match' block"}

def parse_orphan(ctx: ParseContext, lines: list, index: int, decorators: list) -> None:
    """A clause keyword (``else``, ``except``...) with nothing to attach to."""
    first: tools.tokens.TokenInfo = lines[index].first
    raise syntax_error(ctx, _ORPHAN_MESSAGES[first.string], first)

def parse_plain_def(ctx: ParseContext, lines: list, index: int, decorators: list) -> None:
    """Python's ``def`` is not Typy: functions use a typed signature."""
    raise syntax_error(ctx, "'def' is not valid Typy", lines[index].first, hint="declare functions with a typed signature, e.g. 'int add(int a, int b):' or 'void run():'")
