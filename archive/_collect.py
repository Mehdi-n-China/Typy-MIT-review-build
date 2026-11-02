"""Choosing the files an export contains."""
from typing import Any
from .. import tools
from ..ignore import load_ignore_matcher
from ._constants import ARCHIVE_SUFFIX, EXCLUDED_DIRECTORIES

def collect_export_files(root: tools.path.Path) -> list:
    """Every file under ``root`` that belongs in an export, sorted.

    Everything is included except: build output (``root/output``), caches and
    tool folders (``.git``, ``__pycache__``, ...), compiled ``.pyc`` files,
    other ``.typyexp`` archives, and anything ``.typyignore`` excludes. The
    ``.typyignore`` file itself *is* exported, so the recipient builds the
    same project.
    """
    matcher: Any = load_ignore_matcher(root)
    files: list = []
    for directory, subdirectories, names in tools.env.walk(root):
        here: tools.path.Path = tools.path.Path(directory)
        subdirectories[:] = sorted((name for name in subdirectories if name not in EXCLUDED_DIRECTORIES and (not (here == root and name == 'output'))))
        for name in sorted(names):
            path: tools.path.Path = here / name
            relative: tools.path.Path = path.relative_to(root)
            if path.suffix in ('.pyc', ARCHIVE_SUFFIX):
                continue
            if name != '.typyignore' and matcher is not None and matcher.matches(relative.as_posix(), False):
                continue
            files.append(path)
    return files
