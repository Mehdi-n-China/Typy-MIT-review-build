"""Putting freshly parsed nodes back at their real position in the file."""
from typing import Any
from .. import tools

def relocate(tree: Any, real_line: int, col: int, stub_line: int=1) -> None:
    """Shift the locations of ``tree`` (parsed from a snippet of text) so they
    match the original file.

    The snippet's line ``stub_line`` corresponds to ``real_line`` of the file,
    and nodes on that first line also move right by ``col`` columns (the
    snippet was cut from the middle of a line). Every other line only shifts
    vertically, because its text kept its original indentation.
    """
    delta: int = real_line - stub_line
    for node in tools.pyast.walk(tree):
        line: Any = getattr(node, 'lineno', None)
        if line is None:
            continue
        if line == stub_line:
            node.col_offset += col
        end_line: Any = getattr(node, 'end_lineno', None)
        if end_line is not None:
            if end_line == stub_line and node.end_col_offset is not None:
                node.end_col_offset += col
            node.end_lineno = end_line + delta
        node.lineno = line + delta
