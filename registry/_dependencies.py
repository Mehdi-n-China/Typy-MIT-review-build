"""Third-party packages Typy relies on."""
from .. import tools
_DEPENDENCIES: tuple = ('pathspec',)

def installed_dependencies() -> list:
    """``[(name, version_or_None)]`` for each dependency; ``None`` means it is
    not installed."""
    found: list = []
    for name in _DEPENDENCIES:
        try:
            found.append((name, tools.meta.version(name)))
        except tools.meta.PackageNotFoundError:
            found.append((name, None))
    return found
