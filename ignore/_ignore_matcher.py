"""Git-style pattern matching for ``.typyignore``."""
from ._spec import build_spec

class IgnoreMatcher:
    """Answers "is this project path excluded?" using ``.gitignore`` rules:
    globs, ``**``, directory patterns (``build/``), anchoring (``/x``) and
    negation (``!keep.me``).
    """

    def __init__(self: IgnoreMatcher, patterns: list) -> None:
        self._spec = build_spec(patterns)

    def matches(self: IgnoreMatcher, rel_posix_path: str, is_dir: bool) -> bool:
        """True if ``rel_posix_path`` (relative to the project root, with
        ``/`` separators) is ignored. Directories are matched with a trailing
        slash so that directory-only patterns apply to them.
        """
        candidate: str = rel_posix_path + '/' if is_dir else rel_posix_path
        return self._spec.match_file(candidate)
