"""Reading a project's ``.typyignore``."""
from typing import Any
from .. import tools
from ._ignore_matcher import IgnoreMatcher

def load_ignore_matcher(root: tools.path.Path) -> Any:
    """An ``IgnoreMatcher`` for ``root/.typyignore``, or ``None`` if the
    project has no such file."""
    ignore_file: tools.path.Path = root / '.typyignore'
    if not ignore_file.is_file():
        return None
    return IgnoreMatcher(ignore_file.read_text(encoding='utf-8').splitlines())
