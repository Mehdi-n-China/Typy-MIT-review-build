"""Turning the lowered module into source text."""
from typing import Any
from .. import tools
from ..context import CompileContext
from ._fstring_placeholders import extract_fstrings, restore_fstrings
from ._header import build_header
from ._insert_header import insert_header
from ._unparse import unparse_with_spacing

def generate_python(module: Any, ctx: CompileContext) -> str:
    """Add the generated imports to ``module`` and return its Python source.

    F-strings are printed separately (see ``_fstring_render``) so the output
    runs on every supported Python, whichever version ran the compiler.
    """
    tools.pyast.fix_missing_locations(module)
    insert_header(module, build_header(ctx))
    pairs: list = extract_fstrings(module)
    return restore_fstrings(unparse_with_spacing(module.body), pairs, ())
