"""Content digests."""
from .. import tools

def sha256_of(data: bytes) -> str:
    """Hex SHA-256 of ``data`` (bytes)."""
    return tools.hashes.sha256(data).hexdigest()
