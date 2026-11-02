"""Finding the colon that ends a statement header."""
from typing import Any
from .. import tools

def find_header_colon(tokens: list, start: int=0) -> Any:
    """Index of the first ``:`` at or after ``start`` that ends the header.

    Colons inside brackets (slices, dict displays, f-string format specs) are
    skipped by tracking depth, and so is the colon belonging to a ``lambda``
    sitting at the top level of the header. Returns ``None`` if there is no
    header colon.
    """
    depth: int = 0
    pending_lambdas: dict = {}
    for index in range(start, len(tokens)):
        token: tools.tokens.TokenInfo = tokens[index]
        if token.type == tools.tokens.NAME and token.string == 'lambda':
            pending_lambdas[depth] = pending_lambdas.get(depth, 0) + 1
        elif token.type == tools.tokens.OP:
            if token.string in '([{':
                depth += 1
            elif token.string in ')]}':
                depth -= 1
            elif token.string == ':':
                if pending_lambdas.get(depth, 0) > 0:
                    pending_lambdas[depth] -= 1
                elif depth == 0:
                    return index
    return None
