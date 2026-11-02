"""Compiling ignore patterns with ``pathspec``."""
from typing import Any
import pathspec

def build_spec(patterns: list) -> Any:
    """A ``PathSpec`` for gitignore-style ``patterns``.

    ``pathspec`` 1.0 renamed its pattern factory ("gitwildmatch" is now
    deprecated in favour of "gitignore"); the new name is preferred and the
    old one is the fallback for older installs.
    """
    for factory in ('gitignore', 'gitwildmatch'):
        try:
            return pathspec.PathSpec.from_lines(factory, patterns)
        except (KeyError, ValueError):
            continue
    raise RuntimeError("pathspec supports neither the 'gitignore' nor the 'gitwildmatch' pattern factory")
