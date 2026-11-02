"""The closing hint of a build."""
from .. import tools
from ._plan import BuildPlan
from ._reporter import Reporter
from ._stage_compiled import StagedCode

def say_how_to_run(args: tools.args.Namespace, plan: BuildPlan, staged: StagedCode, final: tools.path.Path, report: Reporter) -> None:
    """Tell the user the command that runs what was just built."""
    if args.standalone:
        report.info(f'run it with: python {final}')
    elif staged.entry is not None and (not args.bytecode):
        shown: tools.path.Path = plan.output_dir if staged.entry.name == '__main__.py' else plan.output_dir / staged.entry.name
        report.info(f'run it with: python {shown}')
