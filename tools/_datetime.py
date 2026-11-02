"""datetime facade: wall-clock timestamps for logs and archive manifests."""
from datetime import datetime, timezone
import types
now: types.BuiltinFunctionType = datetime.now

def utc_now_iso() -> str:
    """Current UTC time as an ISO-8601 string with a trailing ``Z``."""
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
