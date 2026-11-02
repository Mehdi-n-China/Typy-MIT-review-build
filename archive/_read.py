"""Reading and verifying an archive."""
from typing import Any
from .. import tools
from ..errors import TypyArchiveError
from ._constants import FORMAT_VERSION, MANIFEST_NAME, PAYLOAD_DIR
from ._hash import sha256_of
from ._safe_path import safe_destination

def read_manifest(archive: Any) -> dict:
    """The validated manifest of an open ``ZipFile``."""
    try:
        manifest: dict = tools.json.loads(archive.read(MANIFEST_NAME))
    except KeyError:
        raise TypyArchiveError(f'not a .typyexp archive: {MANIFEST_NAME} is missing') from None
    except tools.json.JSONDecodeError as error:
        raise TypyArchiveError(f'corrupt manifest: {error}') from None
    if not isinstance(manifest, dict) or not isinstance(manifest.get('files'), list):
        raise TypyArchiveError('corrupt manifest: no file list')
    if manifest.get('format') != FORMAT_VERSION:
        raise TypyArchiveError(f"unsupported archive format {manifest.get('format')!r} (this Typy reads format {FORMAT_VERSION})")
    return manifest

def extract_archive(archive_path: tools.path.Path, destination: tools.path.Path) -> dict:
    """Extract ``archive_path`` into the existing folder ``destination`` and
    return its manifest.

    Every listed file must be present with the recorded size and SHA-256, no
    unlisted file may hide in the payload, and every path is checked against
    ``safe_destination`` before anything is written.
    """
    try:
        with tools.zips.ZipFile(archive_path) as archive:
            manifest: dict = read_manifest(archive)
            listed: set = set()
            for entry in manifest['files']:
                relative: str = entry['path']
                listed.add(f'{PAYLOAD_DIR}/{relative}')
                target: tools.path.Path = safe_destination(destination, relative)
                try:
                    data: bytes = archive.read(f'{PAYLOAD_DIR}/{relative}')
                except KeyError:
                    raise TypyArchiveError(f'archive is missing {relative!r}') from None
                if len(data) != entry['size'] or sha256_of(data) != entry['sha256']:
                    raise TypyArchiveError(f'{relative!r} does not match its recorded checksum; the archive is damaged')
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            stray: list = [name for name in archive.namelist() if name != MANIFEST_NAME and (not name.endswith('/')) and (name not in listed)]
            if stray:
                raise TypyArchiveError(f'archive contains files its manifest does not list: {stray[0]!r}')
    except tools.zips.BadZipFile:
        raise TypyArchiveError('not a valid .typyexp archive (it is not a zip file)') from None
    return manifest
