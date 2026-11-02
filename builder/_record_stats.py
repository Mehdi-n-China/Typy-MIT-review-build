"""Usage counters for ``typy stats``."""
from .. import tools
from ..logger import logger
from ._plan import BuildPlan

def record_build(plan: BuildPlan, args: tools.args.Namespace, file_count: int) -> None:
    """Count a finished build and the options it used."""
    logger.increment_stat('builds')
    logger.increment_stat('files_compiled', file_count)
    logger.increment_stat('single_file_builds' if plan.single_file else 'project_builds')
    for flag in ('enforce', 'gui', 'bytecode', 'standalone', 'lightweight', 'notify'):
        if getattr(args, flag, False):
            logger.increment_stat(f'{flag}_builds')
    logger.log(f'built {file_count} file(s) from {plan.root}')
