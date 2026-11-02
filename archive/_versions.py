"""Comparing dotted version strings."""
from typing import Any
from .. import tools
_VERSION: tools.regex.Pattern = tools.regex.compile('\\d+(?:\\.\\d+)*')

def parse_version(text: Any) -> tuple:
    """``"2.3.9"`` -> ``(2, 3, 9)``; anything that is not a dotted number
    parses as ``(0,)``, i.e. older than every real release."""
    if not isinstance(text, str) or not _VERSION.fullmatch(text):
        return (0,)
    return tuple((int(part) for part in text.split('.')))
