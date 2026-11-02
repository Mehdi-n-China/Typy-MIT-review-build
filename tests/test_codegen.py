"""Shape of the generated Python."""

import unittest

from ._support import compile_ok


class CodegenTests(unittest.TestCase):
    def test_definitions_are_separated_by_blank_lines(self):
        code = compile_ok("int f():\n    return 1\nint x = f()\nint g():\n    return 2\n").python_code
        self.assertIn("return 1\n\nx: int = f()\n\ndef g()", code)

    def test_any_and_dyn_become_typing_any(self):
        code = compile_ok("dyn d = 1\nany a = int('1')\n").python_code
        self.assertTrue(code.startswith("from typing import Any\n"))
        self.assertIn("d: Any = 1", code)

    def test_no_imports_when_none_are_needed(self):
        self.assertEqual(compile_ok("int x = 1\n").python_code, "x: int = 1\n")

    def test_output_is_valid_python(self):
        code = compile_ok(
            "class A:\n    int f(dyn self, *int v, **str k):\n        return 1\n"
            "dyn r = A()?.f(1, a='b')\nunless r:\n    pass\n", enforce=True
        ).python_code
        compile(code, "generated.py", "exec")
