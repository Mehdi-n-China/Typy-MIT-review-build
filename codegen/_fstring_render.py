"""Printing f-strings that every supported Python accepts."""
from typing import Any
from .. import tools
from ._fstring_text import QUOTES, escape_literal
_CONVERSIONS: dict = {114: '!r', 115: '!s', 97: '!a'}

def render_fstring(node: Any, enclosing: tuple=()) -> Any:
    '''Source text for the f-string ``node`` that Python 3.14+ can read, or\n    ``None`` if no choice of quotes works.\n\n    Before 3.12 a replacement field may not contain a backslash or the\n    f-string\'s own quote character, and a nested f-string may not reuse an\n    enclosing one\'s quote. ``ast.unparse`` on 3.12+ ignores those rules, so\n    the quotes are chosen here: the first of ``\'``, ``"``, ``\'\'\'``, ``"""``\n    that every replacement field allows.\n    '''
    taken: set = {quote[0] for quote in enclosing}
    for quote in QUOTES:
        if not quote[0] in taken:
            body: Any = render_parts(node.values, quote, enclosing + (quote,))
            if body is not None:
                return 'f' + quote + body + quote
    return None

def render_parts(values: list, quote: str, enclosing: tuple) -> Any:
    """The text between the quotes, or ``None`` if ``quote`` cannot work."""
    from ._fstring_expression import expression_source
    out: list = []
    for value in values:
        if isinstance(value, tools.pyast.Constant):
            out.append(escape_literal(value.value, quote))
            continue
        text: str = expression_source(value.value, enclosing)
        clash: bool = quote in text if len(quote) == 3 else quote[0] in text
        if '\\' in text or clash:
            return None
        if isinstance(value.value, (tools.pyast.Lambda, tools.pyast.NamedExpr)):
            text = '(' + text + ')'
        if text.startswith('{'):
            text = ' ' + text
        field: str = '{' + text + _CONVERSIONS.get(value.conversion, '')
        if value.format_spec is not None:
            spec: Any = render_parts(value.format_spec.values, quote, enclosing)
            if spec is None:
                return None
            field += ':' + spec
        out.append(field + '}')
    return ''.join(out)
