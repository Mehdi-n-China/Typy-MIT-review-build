"""An f-string rewritten without f-string syntax."""
from typing import Any
from .. import tools
_CONVERTERS: dict = {114: 'repr', 115: 'str', 97: 'ascii'}

def fallback_expression(node: Any) -> tools.pyast.Call:
    """``''.join([...])`` computing exactly what the f-string ``node`` does.

    Used when no quoting lets Python 3.14 read the f-string (a backslash in a
    replacement field, say). ``{x!r:>8}`` becomes ``format(repr(x), '>8')``,
    which is precisely how Python evaluates a replacement field.
    """
    parts: list = []
    for value in node.values:
        if isinstance(value, tools.pyast.Constant):
            parts.append(value)
            continue
        shown: Any = value.value
        if value.conversion in _CONVERTERS:
            converter: tools.pyast.Name = tools.pyast.Name(id=_CONVERTERS[value.conversion], ctx=tools.pyast.Load())
            shown = tools.pyast.Call(func=converter, args=[shown], keywords=[])
        spec: Any = fallback_expression(value.format_spec) if value.format_spec is not None else tools.pyast.Constant(value='')
        formatter: tools.pyast.Name = tools.pyast.Name(id='format', ctx=tools.pyast.Load())
        parts.append(tools.pyast.Call(func=formatter, args=[shown, spec], keywords=[]))
    join: tools.pyast.Attribute = tools.pyast.Attribute(value=tools.pyast.Constant(value=''), attr='join', ctx=tools.pyast.Load())
    return tools.pyast.Call(func=join, args=[tools.pyast.List(elts=parts, ctx=tools.pyast.Load())], keywords=[])
