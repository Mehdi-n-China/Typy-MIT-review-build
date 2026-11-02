"""Writing compiled code into the staging folder."""
from .. import packaging, tools
from ._plan import BuildPlan
from ._reporter import Reporter

class StagedCode:
    """What staging the compiled files produced: whether the runtime is
    needed, which folders hold Python (they become packages), and the
    compiled entry-point file if the plan has one."""

    def __init__(self: StagedCode) -> None:
        self.needs_runtime = False
        self.python_dirs = set()
        self.entry = None
        self.relative_outputs = set()

def stage_compiled_files(plan: BuildPlan, results: list, staging: tools.path.Path, bytecode: bool, report: Reporter) -> StagedCode:
    """Write each compiled file (as ``.py``, or ``.pyc`` with ``--bytecode``),
    mirroring the source layout under ``staging``."""
    staged: StagedCode = StagedCode()
    for path, result in results:
        relative: tools.path.Path = path.relative_to(plan.root).with_suffix('.py')
        target: tools.path.Path = staging / relative
        if bytecode:
            packaging.write_bytecode(result.python_code, target, target.with_suffix('.pyc'))
            report.step(f"wrote {relative.with_suffix('.pyc').as_posix()}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(result.python_code, encoding='utf-8')
            report.step(f'wrote {relative.as_posix()}')
        staged.relative_outputs.add(relative.as_posix())
        staged.python_dirs.add(target.parent)
        staged.needs_runtime = staged.needs_runtime or result.needs_runtime
        if plan.entry is not None and path == plan.entry:
            staged.entry = target
    return staged
