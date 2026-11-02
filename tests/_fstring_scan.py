"""Detecting f-string syntax that only Python 3.12+ can read."""

import io
import tokenize


def pre_312_incompatible_fstrings(code):
    """Lines of ``code`` holding an f-string whose replacement fields reuse an
    enclosing quote or contain a backslash. Needs a 3.12+ tokenizer (which
    splits f-strings into parts); returns nothing on older Pythons."""
    if not hasattr(tokenize, "FSTRING_START"):
        return []
    problems, quotes = [], []
    for token in tokenize.generate_tokens(io.StringIO(code).readline):
        if token.type == tokenize.FSTRING_START:
            quote = token.string.lstrip("rRfFbB")
            if quotes and quote[0] in {q[0] for q in quotes}:
                problems.append(token.line.strip())
            quotes.append(quote)
        elif token.type == tokenize.FSTRING_END:
            quotes.pop()
        elif quotes and token.type == tokenize.STRING:
            if token.string.lstrip("rRbBuU")[0] in {q[0] for q in quotes if len(q) == 1} or "\\" in token.string:
                problems.append(token.line.strip())
    return problems
