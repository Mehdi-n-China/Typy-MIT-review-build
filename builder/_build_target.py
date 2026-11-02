"""The steps of one build, in order."""
from typing import Any
from .. import tools
from ..errors import TypyNotAllowedToOverride, TypyProjectError
from ..packaging import build_standalone
from ._compile_files import compile_files
from ._how_to_run import say_how_to_run
from ._install_runtime import install_runtime
from ._package_markers import add_package_markers
from ._plan import BuildPlan, make_plan
from ._publish import publish_archive, publish_directory
from ._record_stats import record_build
from ._reporter import Reporter
from ._stage_compiled import stage_compiled_files, StagedCode
from ._stage_resources import stage_resource_files

def build_target(args: tools.args.Namespace) -> None:
    """Plan, compile, stage, publish and report one ``typy build``."""
    report: Reporter = Reporter(args.veritasium)
    plan: BuildPlan = make_plan(tools.path.Path(args.target).resolve(), args.lightweight)
    kind: str = 'single file' if plan.single_file else 'project'
    report.step(f'target is a {kind}: {len(plan.typy_files)} .typy file(s), {len(plan.resource_files)} other file(s) to copy' + (' (--lightweight: only .typy/.py)' if args.lightweight else ''))
    if plan.output_dir.exists() and (not args.override):
        raise TypyNotAllowedToOverride(plan.output_dir)
    gui: Any = args.gui and args.enforce
    if args.gui and (not args.enforce):
        report.info('note: --gui monitors --enforce checks; add --enforce, ignoring --gui for this build')
    results: list = compile_files(plan, args.enforce, report)
    with tools.temp.TemporaryDirectory(prefix='typy_build_') as workspace:
        workspace = tools.path.Path(workspace)
        staging: Any = workspace / 'stage'
        staging.mkdir()
        staged: StagedCode = stage_compiled_files(plan, results, staging, args.bytecode, report)
        stage_resource_files(plan, staging, staged, report)
        if not args.bytecode:
            add_package_markers(staged.python_dirs)
        if staged.needs_runtime:
            install_runtime(staging, gui, report)
        elif gui:
            report.info('note: nothing in this program is enforced, so there is nothing for --gui to show')
        if args.standalone:
            if staged.entry is None:
                raise TypyProjectError('--standalone needs an entry point', hint='add a main.typy (or __main__.typy) at the project root')
            archive: tools.path.Path = build_standalone(staging, staged.entry, workspace / f'{plan.name}.pyz')
            final: tools.path.Path = publish_archive(archive, plan.output_dir, args.override)
            report.step(f'packaged the build as {final.name}')
        else:
            publish_directory(staging, plan.output_dir, args.override)
            final = plan.output_dir
    record_build(plan, args, len(results))
    report.info(f'built {len(results)} file(s) -> {final}')
    say_how_to_run(args, plan, staged, final, report)
