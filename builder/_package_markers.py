"""Making output folders importable."""
from typing import Any

def add_package_markers(python_dirs: set) -> None:
    """Give every folder that holds Python an (empty) ``__init__.py`` unless
    it already has one, so the compiled project imports like a package tree."""
    for directory in python_dirs:
        marker: Any = directory / '__init__.py'
        if not marker.exists():
            marker.write_text('', encoding='utf-8')
