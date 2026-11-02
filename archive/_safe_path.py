"""Refusing archive paths that would escape the destination ("zip slip")."""
from typing import Any
from .. import tools
from ..errors import TypyArchiveError

def safe_destination(destination: tools.path.Path, relative: str) -> tools.path.Path:
    """The absolute path for archive member ``relative`` under ``destination``.

    Absolute paths, drive letters, backslashes and any ``..`` component are
    rejected, and the final path is re-checked to still sit inside
    ``destination`` after symlinks are resolved.
    """
    pure: tools.path.PurePosixPath = tools.path.PurePosixPath(relative)
    first: Any = pure.parts[0] if pure.parts else ''
    if not pure.parts or pure.is_absolute() or '..' in pure.parts or ('\\' in relative) or (':' in first):
        raise TypyArchiveError(f'unsafe path in archive: {relative!r}')
    target: tools.path.Path = (destination / pure).resolve()
    if destination.resolve() not in target.parents:
        raise TypyArchiveError(f'archive path escapes the destination: {relative!r}')
    return target
