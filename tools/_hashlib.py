"""hashlib facade: content digests for archive integrity checks."""
import hashlib
import types
sha256: types.BuiltinFunctionType = hashlib.sha256
