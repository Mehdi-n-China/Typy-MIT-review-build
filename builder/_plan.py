"""Deciding what a build covers."""
from typing import Any
from .. import tools
from ..errors import TypyProjectError
from ._walk_project import walk_project

class BuildPlan:
    """What ``typy build`` will do: the files to compile, the files to copy
    along, and where the result goes.

    ``root``        the folder paths are relative to (the project folder, or the
                    folder containing a single target file)
    ``output_dir``  ``root/output``
    ``name``        project or file name; names a standalone archive
    ``entry``       the ``.typy`` file a program starts from, if there is one
    """

    def __init__(self: BuildPlan, root: tools.path.Path, typy_files: list, resource_files: list, single_file: bool) -> None:
        self.root = root
        self.output_dir = root / 'output'
        self.typy_files = typy_files
        self.resource_files = resource_files
        self.single_file = single_file
        self.name = typy_files[0].stem if single_file else root.name
        self.entry = typy_files[0] if single_file else self._find_entry()

    def _find_entry(self: BuildPlan) -> Any:
        for candidate in ('__main__.typy', 'main.typy'):
            if self.root / candidate in self.typy_files:
                return self.root / candidate
        return None

def make_plan(target: tools.path.Path, lightweight: bool=False) -> BuildPlan:
    """Build a ``BuildPlan`` for ``target`` (a ``.typy`` file or a folder)."""
    if target.is_file():
        if target.suffix != '.typy':
            raise TypyProjectError(f'\'{target.name}\' is not a .typy file')
        return BuildPlan(target.parent, [target], [], True)
    if not target.is_dir():
        raise TypyProjectError(f'\'{target}\' is not a file or a directory')
    found: list = list(walk_project(target, lightweight))
    typy_files: list = [path for path, is_typy in found if is_typy]
    if not typy_files:
        raise TypyProjectError(f'no .typy files found under \'{target}\'')
    return BuildPlan(target, typy_files, [path for path, is_typy in found if not is_typy], False)
