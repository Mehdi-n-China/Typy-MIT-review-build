"""Finding the files of a project."""
from typing import Any
from .. import tools
from ..ignore import load_ignore_matcher
_NEVER: frozenset = frozenset({'__pycache__'})

def walk_project(root: tools.path.Path, lightweight: bool=False) -> tools.types.GeneratorType:
    """Yield ``(path, is_typy)`` for every project file that belongs in a build.

    Left out: the top-level ``output/`` folder (the build's own target), hidden
    files and folders (dot-prefixed), ``__pycache__``, compiled ``.pyc`` files,
    ``.typyignore`` itself and anything it excludes. With ``lightweight`` only
    ``.typy`` and ``.py`` files are kept. Excluded folders are pruned, never
    walked into, so huge ignored trees cost nothing.
    """
    matcher: Any = load_ignore_matcher(root)

    def ignored(path: tools.path.Path, is_dir: bool) -> bool:
        return matcher is not None and matcher.matches(path.relative_to(root).as_posix(), is_dir)
    for directory, subdirectories, names in tools.env.walk(root):
        here: tools.path.Path = tools.path.Path(directory)
        subdirectories[:] = sorted((name for name in subdirectories if not name.startswith('.') and name not in _NEVER and (not (here == root and name == 'output')) and (not ignored(here / name, True))))
        for name in sorted(names):
            path: tools.path.Path = here / name
            if name.startswith('.') or path.suffix == '.pyc' or ignored(path, False):
                continue
            is_typy: bool = path.suffix == '.typy'
            if lightweight and (not is_typy) and (path.suffix != '.py'):
                continue
            yield (path, is_typy)
