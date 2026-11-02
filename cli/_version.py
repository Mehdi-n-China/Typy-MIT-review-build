"""``typy version``."""
from .. import __version__, tools
from ._modules_table import format_modules

def cmd_version(args: tools.args.Namespace) -> int:
    """Print the Typy version, the interpreter it runs on and, with
    ``--modules``, the module table."""
    print(f'Typy {__version__.version} (released {__version__.released})')
    print(f'Python {tools.host.python_version()} ({tools.host.python_implementation()}) on {tools.host.system()}')
    if args.modules:
        print('\n'.join(format_modules()))
    return 0
