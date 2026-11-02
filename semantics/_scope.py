"""A Python scope as Typy tracks it."""
from typing import Any

class Scope:
    """One module, function or class scope.

    ``known``     every name the scope binds *anywhere* in its body. Python
                  decides which names are local by scanning the whole body
                  first, and Typy's "declare before assigning" rule uses the
                  same scope-wide view, not source order.
    ``current``   the typed ``Binding`` of each name as of the statement being
                  resolved (source order: redeclaring replaces it).
    ``outer``     names declared ``global`` / ``nonlocal`` here; their real
                  declaration lives in another scope.
    ``voids``     ``void`` functions defined directly in this scope.
    """

    def __init__(self: Scope, kind: Any, parent: Any=None) -> None:
        self.kind = kind
        self.parent = parent
        self.known = set()
        self.current = {}
        self.outer = set()
        self.voids = set()
