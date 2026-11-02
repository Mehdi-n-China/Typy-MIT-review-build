"""Source normalisation."""

def normalize_source(raw: str) -> str:
    """Strip a UTF-8 BOM and convert every newline style to ``\\n``.

    Python's own compiler treats ``\\r\\n`` and ``\\r`` as line ends too, so
    doing this up front keeps every later offset calculation simple.
    """
    if raw.startswith('\ufeff'):
        raw = raw[1:]
    return raw.replace('\r\n', '\n').replace('\r', '\n')
