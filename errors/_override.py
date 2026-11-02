"""Refusing to replace existing output."""
from typing import Any
from .. import tools
from ._base import TypyBaseError

class TypyNotAllowedToOverride(TypyBaseError):
    """The output already exists and --override was not given."""

    def __init__(self: Any, output_dir: tools.path.Path) -> None:
        super().__init__(f'\'{output_dir}\' already exists. Pass --override to replace it.', hint='re-run with --override if replacing it is what you want')
