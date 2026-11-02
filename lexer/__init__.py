"""
Typy lexer: source text -> a tree of logical lines.

Python's own tokenizer does the character-level work (strings, numbers,
operators, brackets, indentation). This package adds what Typy needs on top:

    * newline/BOM normalisation and the "no tabs" rule
    * grouping tokens into *logical lines* nested by indentation
    * small token-stream helpers the parser leans on (bracket matching,
      header colons, dotted type names)

Since: 0.1.0
"""
from ._brackets import find_closing_bracket, split_top_level
from ._dotted_name import read_dotted_name
from ._header_colon import find_header_colon
from ._lex import LexedSource, lex_source
from ._logical_line import LogicalLine
from ._source_text import SourceText
