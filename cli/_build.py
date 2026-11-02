"""``typy build``."""
from .. import tools
from ..builder import run_build
from ..errors import TypyFlagConflict
from ..notifications import notify

def cmd_build(args: tools.args.Namespace) -> int:
    """Validate flag combinations, build, and notify if asked.

    ``--bytecode`` and ``--standalone`` are the one explicitly incompatible
    pair (both choose the output format); every other flag is independent.
    """
    if args.bytecode and args.standalone:
        raise TypyFlagConflict(['--bytecode', '--standalone'])
    run_build(args)
    if args.notify:
        notify()
    return 0
