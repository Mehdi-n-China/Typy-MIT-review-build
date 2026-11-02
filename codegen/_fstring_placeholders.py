"""Taking f-strings out of a tree before printing, and putting them back."""
from typing import Any
from .. import tools

def extract_fstrings(tree: Any) -> list:
    """Replace every outermost f-string in ``tree`` with a placeholder name
    and return ``[(placeholder, f-string node)]``.

    ``ast.unparse`` then prints everything else, and ``restore_fstrings``
    swaps each placeholder for an f-string printed by ``render_fstring``.
    """
    pairs: list = []
    stack: list = [tree]
    while stack:
        node: Any = stack.pop()
        for name, value in tools.pyast.iter_fields(node):
            items: Any = value if isinstance(value, list) else [value]
            for index, item in enumerate(items):
                if isinstance(item, tools.pyast.JoinedStr):
                    placeholder: tools.pyast.Name = tools.pyast.Name(id=f'__typy_fstring_{len(pairs)}__', ctx=tools.pyast.Load())
                    pairs.append((placeholder.id, item))
                    if isinstance(value, list):
                        value[index] = placeholder
                    else:
                        setattr(node, name, placeholder)
                elif isinstance(item, tools.pyast.AST):
                    stack.append(item)
    return pairs

def restore_fstrings(text: str, pairs: list, enclosing: tuple) -> str:
    """Put printed f-strings back in place of their placeholders. An f-string
    no quoting can express is printed as its ``''.join`` equivalent."""
    from ._fstring_expression import expression_source
    from ._fstring_fallback import fallback_expression
    from ._fstring_render import render_fstring
    for placeholder, node in pairs:
        rendered: Any = render_fstring(node, enclosing)
        if rendered is None:
            rendered = expression_source(fallback_expression(node), enclosing)
        text = text.replace(placeholder, rendered, 1)
    return text
