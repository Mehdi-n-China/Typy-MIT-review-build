"""Runtime enforcement with --enforce (spec §10-12)."""

import unittest

from ._support import compile_ok, run_typy, use_runtime


class EnforcementTests(unittest.TestCase):
    def setUp(self):
        use_runtime()
        from _typy_runtime import TypyTypeError

        self.error = TypyTypeError

    def test_without_enforce_nothing_is_checked(self):
        result = compile_ok("int x = 5\nx = 'no checks'\n")
        self.assertFalse(result.needs_runtime)
        self.assertEqual(run_typy("int x = 5\nx = 'no checks'\n")["x"], "no checks")

    def test_declared_types_are_exact(self):
        for source in ("int x = 5\nx = 'a'\n", "int x = 5\nx = True\n", "bool b = True\nb = 1\n"):
            with self.subTest(source=source), self.assertRaises(self.error):
                run_typy(source, enforce=True)

    def test_subclasses_do_not_satisfy_the_parent(self):
        with self.assertRaises(self.error):
            run_typy("class A:\n    pass\nclass B(A):\n    pass\nA a = A()\na = B()\n", enforce=True)

    def test_any_establishes_then_enforces(self):
        self.assertEqual(run_typy("any x = 5\nx = 6\n", enforce=True)["x"], 6)
        with self.assertRaises(self.error):
            run_typy("any x = 5\nx = 'a'\n", enforce=True)

    def test_any_with_a_literal_is_resolved_at_compile_time(self):
        code = compile_ok("any x = 5\nx = 6\n", enforce=True).python_code
        self.assertIn("typy.check(5, int, 'x')", code)
        self.assertNotIn("AnyState", code)

    def test_any_with_a_non_literal_value(self):
        with self.assertRaises(self.error):
            run_typy("any x = int('5')\nx = 5.0\n", enforce=True)

    def test_dyn_is_never_checked(self):
        self.assertEqual(run_typy("dyn x = 5\nx = 'a'\nx = [1]\n", enforce=True)["x"], [1])

    def test_augmented_assignment_is_rechecked(self):
        with self.assertRaises(self.error):
            run_typy("int total = 1\ntotal += 1.5\n", enforce=True)

    def test_parameters(self):
        ns = run_typy("int f(int a, any b, dyn c):\n    return a\n", enforce=True)
        self.assertEqual(ns["f"](1, "x", None), 1)
        with self.assertRaises(self.error):
            ns["f"]("1", "x", None)

    def test_variadic_elements(self):
        ns = run_typy("int f(*int values, **str named):\n    return 0\n", enforce=True)
        ns["f"](1, 2, a="x")
        with self.assertRaises(self.error):
            ns["f"](1, "2")
        with self.assertRaises(self.error):
            ns["f"](a=1)

    def test_return_values(self):
        ns = run_typy("int good():\n    return 1\nint bad():\n    return 'x'\nint missing():\n    pass\n", enforce=True)
        self.assertEqual(ns["good"](), 1)
        for name in ("bad", "missing"):
            with self.subTest(name=name), self.assertRaises(self.error):
                ns[name]()

    def test_none_functions_must_return_none(self):
        ns = run_typy("None ok():\n    return\nNone bad():\n    return 1\n", enforce=True)
        self.assertIsNone(ns["ok"]())
        with self.assertRaises(self.error):
            ns["bad"]()

    def test_generators_are_not_return_checked(self):
        ns = run_typy("list gen():\n    yield 1\n", enforce=True)
        self.assertEqual(list(ns["gen"]()), [1])

    def test_none_typed_variable(self):
        with self.assertRaises(self.error):
            run_typy("None n = None\nn = 1\n", enforce=True)

    def test_runtime_import_follows_the_docstring_and_future_imports(self):
        code = compile_ok('"""Doc."""\nfrom __future__ import annotations\nint x = 1\n', enforce=True).python_code
        lines = code.splitlines()
        self.assertEqual(lines[0], "\"\"\"Doc.\"\"\"")
        self.assertEqual(lines[1], "from __future__ import annotations")
        self.assertEqual(lines[2], "import _typy_runtime as typy")
