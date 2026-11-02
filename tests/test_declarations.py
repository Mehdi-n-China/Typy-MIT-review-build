"""Typed declarations and the declare-before-assigning rule (spec §5-8)."""

import unittest

from ._support import compile_errors, compile_ok, run_typy


class DeclarationTests(unittest.TestCase):
    def test_basic_types(self):
        ns = run_typy('int x = 10\nstr s = "hi"\nfloat f = 1.5\nbool b = True\nNone n = None\n')
        self.assertEqual((ns["x"], ns["s"], ns["n"]), (10, "hi", None))

    def test_generates_annotations(self):
        self.assertIn("x: int = 10", compile_ok("int x = 10\n").python_code)

    def test_nested_qualified_type(self):
        ns = run_typy("class Parent:\n    class Car:\n        pass\n\nParent.Car car = Parent.Car()\n")
        self.assertIsInstance(ns["car"], ns["Parent"].Car)

    def test_literal_mismatch(self):
        for source in ("int x = 10.5\n", "bool b = 1\n", "str s = None\n", "list l = (1,)\n", "Ellipsis e = 1\n"):
            with self.subTest(source=source):
                self.assertTrue(any("type mismatch" in e for e in compile_errors(source)))

    def test_literal_matches(self):
        compile_ok("int x = -5\ncomplex z = 3+4j\ndict d = {}\nbytes b = b''\nEllipsis e = ...\n")

    def test_arbitrary_expressions_are_trusted(self):
        compile_ok("Car c = make_car()\nint x = 1 + 2\n")

    def test_undeclared_assignment(self):
        self.assertTrue(any("not declared" in e for e in compile_errors("x = 10\n")))

    def test_unpacking_needs_declarations_too(self):
        self.assertEqual(len(compile_errors("a, b = 1, 2\n")), 2)

    def test_declare_then_reassign(self):
        self.assertEqual(run_typy("int x = 10\nx = 20\n")["x"], 20)

    def test_declaration_order_inside_a_scope_does_not_matter(self):
        compile_ok("for i in range(2):\n    x = i\nint x = 0\n")

    def test_other_bindings_count_as_declarations(self):
        compile_ok(
            "import os\nfor a in []:\n    a = 1\nwith open(__file__) as f:\n    f = None\n"
            "try:\n    pass\nexcept Exception as e:\n    e = None\n(w := 1)\nw = 2\n"
        )

    def test_global_and_nonlocal(self):
        compile_ok("int counter = 0\nvoid bump():\n    global counter\n    counter = counter + 1\n")

    def test_redeclaration_replaces_type_information(self):
        ns = run_typy('int x = 1\nstr x = "now a string"\nx = "fine"\n', enforce=True)
        self.assertEqual(ns["x"], "fine")

    def test_python_style_annotations(self):
        compile_ok("x: int\ny: int = 5\ny = 6\n")

    def test_errors_are_all_reported_and_sorted(self):
        errors = compile_errors("b = 1\nint x = 1.5\na = 2\n")
        self.assertEqual(len(errors), 3)
        self.assertEqual([e.split(":")[1] for e in errors], ["line-1", "line-2", "line-3"])
