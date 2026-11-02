"""``typy export``."""
from .. import tools
from ..archive import ARCHIVE_SUFFIX, collect_export_files, write_archive
from ..errors import TypyArchiveError, TypyNotAllowedToOverride, TypyProjectError
from ..logger import logger

def cmd_export(args: tools.args.Namespace) -> int:
    """Package a project folder as a ``.typyexp`` archive.

    The archive is written under a temporary name and renamed into place, so
    an interrupted export never leaves a half-written file behind.
    """
    root: tools.path.Path = tools.path.Path(args.target).resolve()
    if not root.is_dir():
        raise TypyProjectError(f'\'{root}\' is not a project directory')
    destination: tools.path.Path = tools.path.Path(args.output).resolve() if args.output else root.parent / f'{root.name}{ARCHIVE_SUFFIX}'
    if destination.exists() and (not args.override):
        raise TypyNotAllowedToOverride(destination)
    files: list = collect_export_files(root)
    if not files:
        raise TypyArchiveError(f'nothing to export: \'{root}\' has no files')
    partial: tools.path.Path = destination.with_name(destination.name + '.partial')
    write_archive(root, files, partial)
    partial.replace(destination)
    logger.increment_stat('exports')
    logger.log(f'exported {root} -> {destination}')
    size_kb: float = destination.stat().st_size / 1024
    print(f'exported {len(files)} file(s) ({size_kb:.1f} KB) -> {destination}')
    return 0
