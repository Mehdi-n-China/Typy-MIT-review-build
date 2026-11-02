"""Copying a project's non-Typy files into the staging folder."""
from .. import tools
from ..errors import TypyProjectError
from ._plan import BuildPlan
from ._reporter import Reporter
from ._stage_compiled import StagedCode

def stage_resource_files(plan: BuildPlan, staging: tools.path.Path, staged: StagedCode, report: Reporter) -> None:
    """Copy every resource file (images, data, plain ``.py``...) to the same
    relative place in ``staging``.

    A plain ``.py`` that would land on a compiled file's output path (say
    ``util.typy`` and ``util.py`` side by side) is refused instead of one
    silently overwriting the other.
    """
    for path in plan.resource_files:
        relative: tools.path.Path = path.relative_to(plan.root)
        if relative.as_posix() in staged.relative_outputs:
            raise TypyProjectError(f"'{relative.as_posix()}' would overwrite the compiled output of '{relative.with_suffix('.typy').as_posix()}'", hint='rename one of the two files')
        target: tools.path.Path = staging / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        tools.fs.copyfile(path, target)
        if target.suffix == '.py':
            staged.python_dirs.add(target.parent)
        report.step(f'copied {relative.as_posix()}')
