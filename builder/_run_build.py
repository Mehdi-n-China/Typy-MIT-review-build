"""The build sequence."""
from .. import tools
from ..errors import TypyBaseError
from ..logger import logger
from ._build_target import build_target

def run_build(args: tools.args.Namespace) -> None:
    """Run ``typy build`` for the parsed command line ``args``.

    Order matters for safety: the override check and every compile happen
    before anything is written; output is then staged in a temporary folder
    and copied into ``output/`` last. Raises a ``TypyBaseError`` on failure
    (and counts it for ``typy stats``).
    """
    try:
        build_target(args)
    except TypyBaseError:
        logger.increment_stat('failed_builds')
        raise
