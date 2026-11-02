"""Quotes and escaping for printed f-strings."""
QUOTES: tuple = ("'", '"', "'''", '"""')
_SHORT_ESCAPES: dict = {'\n': '\\n', '\r': '\\r', '\t': '\\t'}

def escape_literal(text: str, quote: str) -> str:
    """Escape a literal part of an f-string delimited by ``quote``.

    Backslashes, control characters and the quote character are escaped and
    braces are doubled, so the text means the same once it is inside
    ``f<quote>...<quote>``. Everything else, non-ASCII included, is kept.
    """
    out: list = []
    for char in text:
        if char == '\\':
            out.append('\\\\')
        elif char in '{}':
            out.append(char * 2)
        elif char in _SHORT_ESCAPES:
            out.append(_SHORT_ESCAPES[char])
        elif ord(char) < 32 or ord(char) == 127:
            out.append('\\x%02x' % ord(char))
        elif char == quote[0]:
            out.append('\\' + char)
        else:
            out.append(char)
    return ''.join(out)
