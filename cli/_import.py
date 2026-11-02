"""``typy import``."""
from .. import __version__, tools
from ..archive import extract_archive, parse_version
from ..errors import TypyArchiveError, TypyNotAllowedToOverride
from ..logger import logger

def cmd_import(args: tools.args.Namespace) -> int:
    """Unpack a ``.typyexp`` archive into a project folder.

    Everything is extracted and verified in a temporary folder first; the
    destination is only created (or, with ``--override``, replaced) once the
    whole archive has checked out.
    """
    archive: tools.path.Path = tools.path.Path(args.target).resolve()
    if not archive.is_file():
        raise TypyArchiveError(f'\'{archive}\' is not a file')
    destination: tools.path.Path = tools.path.Path(args.output).resolve() if args.output else archive.parent / archive.stem
    if destination == archive:
        destination = archive.parent / f'{archive.name}_imported'
    if destination.exists() and (not args.override):
        raise TypyNotAllowedToOverride(destination)
    with tools.temp.TemporaryDirectory(prefix='typy_import_') as workspace:
        staging: tools.path.Path = tools.path.Path(workspace) / 'project'
        staging.mkdir()
        manifest: dict = extract_archive(archive, staging)
        if destination.exists():
            tools.fs.rmtree(destination)
        tools.fs.move(str(staging), str(destination))
    if parse_version(manifest.get('typy')) > parse_version(__version__.version):
        print(f"note: this archive was made by Typy {manifest.get('typy')}; you have {__version__.version}")
    logger.increment_stat('imports')
    logger.log(f'imported {archive} -> {destination}')
    print(f"imported {len(manifest['files'])} file(s) -> {destination}")
    return 0
