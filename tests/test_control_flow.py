"""until / forever / repeat / unless / elunless / initialized loops (spec §17-23)."""

import unittest

from ._support import compile_errors, compile_ok, run_typy


class ControlFlowTests(unittest.TestCase):
    def test_until(self):
        self.assertEqual(run_typy("int i = 0\nuntil i >= 3:\n    i += 1\n")["i"], 3)

    def test_until_else(self):
        ns = run_typy("int i = 0\nstr r = ''\nuntil i >= 2:\n    i += 1\nelse:\n    r = 'done'\n")
        self.assertEqual(ns["r"], "done")

    def test_forever_with_break(self):
        self.assertEqual(run_typy("int i = 0\nforever:\n    i += 1\n    if i >= 3:\n        break\n")["i"], 3)

    def test_repeat_uses_the_reserved_double_underscore(self):
        result = compile_ok("int c = 0\nrepeat 5:\n    c = c + 1\n")
        self.assertIn("for __ in range(5):", result.python_code)
        self.assertEqual(run_typy("int c = 0\nrepeat 5:\n    c = c + 1\n")["c"], 5)

    def test_nested_repeat(self):
        self.assertEqual(run_typy("int c = 0\nrepeat 3:\n    repeat 4:\n        c += 1\n")["c"], 12)

    def test_single_underscore_is_an_ordinary_name(self):
        ns = run_typy("dyn total = 0\nfor _ in range(3):\n    total += 1\ndyn pair = (1, 2)\ndyn first = 0\nfirst, _ = pair\n")
        self.assertEqual((ns["total"], ns["first"]), (3, 1))

    def test_unless_chain(self):
        source = "int x = 5\nstr r = ''\n{0} x > 10:\n    r = 'a'\nelunless x < 0:\n    r = 'b'\nelse:\n    r = 'c'\n"
        self.assertEqual(run_typy(source.format("unless"))["r"], "a")
        self.assertEqual(run_typy(source.format("if"))["r"], "b")

    def test_unless_negates_the_whole_condition(self):
        self.assertEqual(run_typy("int r = 0\nunless True or False:\n    r = 1\nelse:\n    r = 2\n")["r"], 2)

    def test_initialized_while(self):
        ns = run_typy("int total = 0\ni(0) while i < 5:\n    total += i\n    i += 1\n")
        self.assertEqual(ns["total"], 10)
        self.assertNotIn("i", ns)

    def test_initialized_until_with_two_variables(self):
        ns = run_typy("int steps = 0\ni(0), j(10) until i >= j:\n    i += 1\n    j -= 1\n    steps += 1\n")
        self.assertEqual(ns["steps"], 5)
        self.assertNotIn("j", ns)

    def test_loop_variables_are_deleted_after_break_and_exceptions(self):
        ns = run_typy("i(0) while True:\n    break\n")
        self.assertNotIn("i", ns)
        with self.assertRaises(ZeroDivisionError):
            run_typy("i(0) while True:\n    i = 1 / 0\n")

    def test_nested_initialized_loops(self):
        ns = run_typy("int total = 0\ni(0) while i < 3:\n    j(0) while j < 2:\n        total += 1\n        j += 1\n    i += 1\n")
        self.assertEqual(ns["total"], 6)

    def test_bad_loop_headers(self):
        for source in ("forever x:\n    pass\n", "repeat:\n    pass\n", "i() while i:\n    pass\n", "i(0), i(1) while i:\n    pass\n"):
            with self.subTest(source=source):
                self.assertTrue(compile_errors(source))
