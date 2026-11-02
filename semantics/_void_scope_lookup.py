"""Does a bare name refer to a ``void`` function?"""
from typing import Any
from ._scope import Scope

def refers_to_void(scope: Scope, name: str) -> bool:
    """Resolve ``name`` the way Python would and say whether the function it
    finds was declared ``void``.

    The nearest scope that binds the name decides, so a local variable
    shadowing a void function correctly stops the check. A class body is only
    visible from itself, never from the functions nested inside it.
    """
    current: Any = scope
    first: bool = True
    while current is not None:
        if current.kind != 'class' or first:
            if name in current.voids:
                return True
            if name in current.known:
                return False
        current = current.parent
        first = False
    return False
