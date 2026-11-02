"""Simple statements: one logical line may hold several, split by ``;``."""
from typing import Any
from ..lexer import split_top_level
from ._bridge import parse_python_statements
from ._missing_value import reject_declaration_without_value
from ._typed_declaration import match_typed_declaration, parse_typed_declaration
from ._context import ParseContext

def parse_segment(ctx: ParseContext, tokens: list) -> list:
    """Parse one simple statement: a typed declaration if it looks like one,
    otherwise plain Python. Returns a list of statement nodes."""
    match: Any = match_typed_declaration(tokens)
    if match is not None:
        return [parse_typed_declaration(ctx, tokens, match)]
    reject_declaration_without_value(ctx, tokens)
    return parse_python_statements(ctx, tokens)

def parse_segments(ctx: ParseContext, tokens: list) -> list:
    """Parse a run of simple statements separated by top-level ``;``."""
    statements: list = []
    for segment in split_top_level(tokens, ';'):
        if segment:
            statements.extend(parse_segment(ctx, segment))
    return statements
