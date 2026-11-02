"""The manifest stored inside every archive."""
from .. import __version__, tools
from ._constants import FORMAT_VERSION
from ._hash import sha256_of

def build_manifest(root: tools.path.Path, files: list) -> dict:
    """Describe ``files`` (paths under ``root``): their relative path, size
    and SHA-256, plus the format version, the Typy version and a UTC time."""
    entries: list = []
    for path in files:
        data: bytes = path.read_bytes()
        entries.append({'path': path.relative_to(root).as_posix(), 'size': len(data), 'sha256': sha256_of(data)})
    return {'format': FORMAT_VERSION, 'typy': __version__.version, 'name': root.name, 'created': tools.date.utc_now_iso(), 'files': entries}
