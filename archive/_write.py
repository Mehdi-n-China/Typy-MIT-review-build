"""Writing an archive."""
from .. import tools
from ._constants import MANIFEST_NAME, PAYLOAD_DIR
from ._manifest import build_manifest

def write_archive(root: tools.path.Path, files: list, destination: tools.path.Path) -> dict:
    """Write ``files`` (paths under ``root``) to the zip at ``destination``
    and return the manifest that was stored.

    The manifest goes first so a reader can validate before touching the
    payload; payload paths always use ``/`` regardless of the host system.
    """
    manifest: dict = build_manifest(root, files)
    with tools.zips.ZipFile(destination, 'w', tools.zips.ZIP_DEFLATED) as archive:
        archive.writestr(MANIFEST_NAME, tools.json.dumps(manifest, indent=2))
        for path in files:
            archive.write(path, f'{PAYLOAD_DIR}/{path.relative_to(root).as_posix()}')
    return manifest
