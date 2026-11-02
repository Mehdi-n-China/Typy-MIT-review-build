"""The lexer: logical lines, tabs, delimiters, internal names."""

import unittest

from ..errors import TypyIndentationError, TypySyntaxError
from ..lexer import lex_source


class LexerTests(unittest.TestCase):
    def test_logical_lines_nest_by_indentation(self):
        lexed = lex_source("if x:\n    y = (1,\n         2)\n    # comment\n\nz = 3\n")
        self.assertEqual(len(lexed.lines), 2)
        self.assertEqual(len(lexed.lines[0].children), 1)
        self.assertEqual(lexed.lines[1].line, 6)

    def test_tabs_are_rejected(self):
        with self.assertRaises(TypyIndentationError):
            lex_source("if x:\n\tpass\n")

    def test_tabs_inside_strings_are_fine(self):
        lex_source('s = "a\\tb\tc"\n')

    def test_unclosed_bracket_is_a_syntax_error(self):
        with self.assertRaises(TypySyntaxError):
            lex_source("x = (1, 2\n")

    def test_unexpected_indent(self):
        with self.assertRaises(TypyIndentationError):
            lex_source("    x = 1\n")

    def test_chain_guard_name_is_reserved_for_the_compiler(self):
        with self.assertRaises(TypySyntaxError):
            lex_source("x.__typyg__\n")

    def test_crlf_and_bom_are_normalised(self):
        lexed = lex_source("\ufeffint x = 1\r\nint y = 2\r\n")
        self.assertEqual(len(lexed.lines), 2)
        self.assertIn("x", lexed.names)
