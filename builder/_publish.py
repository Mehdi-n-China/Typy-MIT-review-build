"""Moving a finished build into ``output/``."""
from .. import tools
from ._clear_destination import clear_destination

def publish_directory(staging: tools.path.Path, output_dir: tools.path.Path, override: bool) -> None:
    """Replace ``output_dir`` with the contents of ``staging``."""
    clear_destination(output_dir, override)
    tools.fs.copytree(staging, output_dir)

def publish_archive(archive: tools.path.Path, output_dir: tools.path.Path, override: bool) -> tools.path.Path:
    """Replace ``output_dir`` with a folder holding just the archive file
    (``--standalone`` ships one runnable file, not the loose sources)."""
    clear_destination(output_dir, override)
    output_dir.mkdir(parents=True)
    tools.fs.copy2(archive, output_dir / archive.name)
    return output_dir / archive.name
