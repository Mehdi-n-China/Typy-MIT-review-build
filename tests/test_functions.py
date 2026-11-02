"""Typed functions, void and None (spec §13-15)."""

import unittest

from ._support import compile_errors, compile_ok, run_typy


class FunctionTests(unittest.TestCase):
    def test_typed_function(self):
        self.assertEqual(run_typy("int square(int n):\n    return n * n\n")["square"](5), 25)

    def test_generated_header(self):
        code = compile_ok("int add(int a, /, int b = 5, *, str c = 'k', **float rest):\n    return a\n").python_code
        self.assertIn("def add(a: int, /, b: int=5, *, c: str='k', **rest: float) -> int:", code)

    def test_positional_only_and_keyword_only_behave_like_python(self):
        ns = run_typy("int f(int a, /, int b, *, int c):\n    return a + b + c\n")
        self.assertEqual(ns["f"](1, 2, c=3), 6)
        with self.assertRaises(TypeError):
            ns["f"](a=1, b=2, c=3)
        with self.assertRaises(TypeError):
            ns["f"](1, 2, 3)

    def test_variadics(self):
        ns = run_typy("int total(*int values, **str labels):\n    return sum(values) + len(labels)\n")
        self.assertEqual(ns["total"](1, 2, a="x"), 4)

    def test_void_rules(self):
        self.assertTrue(compile_errors("void f():\n    return\n"))
        self.assertTrue(compile_errors("void f():\n    return 5\n"))
        for use in ("int x = f()\n", "print(f())\n", "g(f())\n", "int h():\n    return f()\n"):
            with self.subTest(use=use):
                self.assertTrue(compile_errors("void f():\n    pass\n\n" + use))

    def test_void_standalone_call(self):
        compile_ok("void f():\n    pass\n\nf()\n")

    def test_void_call_can_be_awaited_as_a_statement(self):
        compile_ok("async void f():\n    pass\n\nasync void g():\n    await f()\n")

    def test_void_lookup_respects_shadowing(self):
        compile_ok("void f():\n    pass\n\nint g(int f):\n    return f()\n")

    def test_return_inside_nested_function_of_void_is_fine(self):
        compile_ok("void outer():\n    int inner():\n        return 1\n    inner()\n")

    def test_none_return_type(self):
        self.assertIsNone(run_typy("None f():\n    return\n")["f"]())
        compile_ok("None f():\n    return None\n")

    def test_void_lowers_to_none_annotation(self):
        self.assertIn("-> None", compile_ok("void f():\n    pass\n").python_code)

    def test_methods_and_docstrings(self):
        ns = run_typy(
            'class Car:\n    None __init__(dyn self, int wheels):\n        self.wheels = wheels\n'
            '    int count(dyn self):\n        """How many wheels."""\n        return self.wheels\n',
            enforce=True,
        )
        car = ns["Car"](4)
        self.assertEqual(car.count(), 4)
        self.assertEqual(ns["Car"].count.__doc__, "How many wheels.")

    def test_default_literal_mismatch(self):
        self.assertTrue(compile_errors("int f(int x = 1.5):\n    return x\n"))
