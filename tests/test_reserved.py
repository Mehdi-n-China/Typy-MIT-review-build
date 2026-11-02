"""Reserved identifiers (spec §4)."""

import unittest

from ._support import compile_errors, compile_ok


class ReservedTests(unittest.TestCase):
    def test_reserved_names_cannot_be_defined(self):
        sources = [
            "int typy = 5\n", "int __ = 1\n", "dyn any = 1\n", "for until in []:\n    pass\n",
            "void repeat():\n    pass\n", "int f(int void):\n    return 1\n", "import os as dyn\n",
            "class forever:\n    pass\n", "until(0) while True:\n    pass\n",
        ]
        for source in sources:
            with self.subTest(source=source):
                self.assertTrue(compile_errors(source))

    def test_referencing_builtin_any_is_fine(self):
        compile_ok("bool b = any([True])\n")

    def test_names_merely_starting_with_underscores_are_fine(self):
        compile_ok("int _temp = 5\nint __internal = 6\nint _ = 7\n")
