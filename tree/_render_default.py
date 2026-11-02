"""Printing default-value expressions for display."""
from typing import Any
from .. import tools

def render_default(node: Any) -> str:
    """Source text for a default-value expression.

    Used only for display (``Parameter.formatted``, verbose build output).
    Expressions that still contain Typy-only nodes cannot be unparsed by
    ``ast`` yet, so they are shown as ``...``.
    """
    try:
        return tools.pyast.unparse(node)
    except Exception:
        return '...'
