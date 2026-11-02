"""Argument parser configuration."""
from typing import Any
from .. import __version__, tools
from ._build import cmd_build
from ._export import cmd_export
from ._import import cmd_import
from ._stats import cmd_stats
from ._version import cmd_version

def build_arg_parser() -> tools.args.ArgumentParser:
    """The ``typy`` parser with one sub-parser per command."""
    parser: tools.args.ArgumentParser = tools.args.ArgumentParser(prog='typy', description=f'Typy compiler v{__version__.version}.')
    sub: Any = parser.add_subparsers(dest='command', required=True)
    build_parser: tools.args.ArgumentParser = sub.add_parser(name='build', help='compile a .typy file or project directory')
    build_parser.add_argument('target', help='target a .typy file or a project directory')
    build_parser.add_argument('--enforce', action='store_true', help='runtime type enforcement')
    build_parser.add_argument('--gui', action='store_true', help='attach the enforcement monitor (needs --enforce)')
    build_parser.add_argument('--override', action='store_true', help='replace an existing output/ folder')
    build_parser.add_argument('--bytecode', action='store_true', help='compile to .pyc instead of .py')
    build_parser.add_argument('--standalone', action='store_true', help='compile to a single self-contained runnable archive')
    build_parser.add_argument('--lightweight', action='store_true', help='only copy .typy/.py project files')
    build_parser.add_argument('--veritasium', action='store_true', help='verbose compiler diagnostics')
    build_parser.add_argument('--notify', action='store_true', help='beep on completion')
    build_parser.set_defaults(func=cmd_build)
    export_parser: tools.args.ArgumentParser = sub.add_parser(name='export', help='export a project as a .typyexp file')
    export_parser.add_argument('target', help='target a project directory')
    export_parser.add_argument('-o', '--output', help='archive path (default: <project>.typyexp next to the project)')
    export_parser.add_argument('--override', action='store_true', help='replace an existing archive')
    export_parser.set_defaults(func=cmd_export)
    import_parser: tools.args.ArgumentParser = sub.add_parser(name='import', help='import a project from a .typyexp file')
    import_parser.add_argument('target', help='target a .typyexp file')
    import_parser.add_argument('-o', '--output', help='project folder (default: the archive name, next to it)')
    import_parser.add_argument('--override', action='store_true', help='replace an existing project folder entirely')
    import_parser.set_defaults(func=cmd_import)
    stats_parser: tools.args.ArgumentParser = sub.add_parser(name='stats', help='shows your Typy stats')
    stats_parser.add_argument('--json', action='store_true', help='print the raw counters as JSON')
    stats_parser.add_argument('--reset', action='store_true', help='set every counter back to zero')
    stats_parser.set_defaults(func=cmd_stats)
    version_parser: tools.args.ArgumentParser = sub.add_parser(name='version', help='show typy version')
    version_parser.add_argument('--modules', action='store_true', help='show modules')
    version_parser.set_defaults(func=cmd_version)
    return parser
