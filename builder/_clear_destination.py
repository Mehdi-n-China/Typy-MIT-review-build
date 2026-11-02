"""Making room for a new build."""
from .. import tools
from ..errors import TypyNotAllowedToOverride

def clear_destination(output_dir: tools.path.Path, override: bool) -> None:
    """Remove an existing ``output_dir`` if ``--override`` allows it, or refuse."""
    if output_dir.exists():
        if not override:
            raise TypyNotAllowedToOverride(output_dir)
        tools.fs.rmtree(output_dir)
