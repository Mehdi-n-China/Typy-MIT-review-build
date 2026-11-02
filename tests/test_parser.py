"""The parser builds the Typy AST."""

import ast
import unittest

from ..errors import TypyIndentationError, TypySyntaxError
from ..parser import parse_source
from ..tree import (
    Conditional, ForeverLoop, FunctionDeclaration, InitializedLoop, OptionalChain,
    ParameterKind, RepeatLoop, TypedDeclaration, UntilLoop,
)


def body(source):
    return parse_source(source, "test.typy")[0].body


class ParserTests(unittest.TestCase):
    def test_each_typy_statement_becomes_its_node(self):
        nodes = body(
            "int x = 1\nvoid f():\n    pass\nunless x:\n    pass\nuntil x:\n    pass\n"
            "forever:\n    break\nrepeat 3:\n    pass\ni(0) while i < 3:\n    i += 1\n"
        )
        kinds = [type(node) for node in nodes]
        self.assertEqual(
            kinds,
            [TypedDeclaration, FunctionDeclaration, Conditional, UntilLoop, ForeverLoop, RepeatLoop, InitializedLoop],
        )

    def test_plain_python_stays_python(self):
        nodes = body("print(1)\nfor a in b:\n    pass\nwith c as d:\n    pass\nclass K:\n    pass\n")
        self.assertEqual([type(n) for n in nodes], [ast.Expr, ast.For, ast.With, ast.ClassDef])

    def test_locations_point_into_the_source(self):
        nodes = body("\n\nint x = 1\nint y = (2 +\n         3)\n")
        self.assertEqual((nodes[0].lineno, nodes[1].lineno), (3, 4))

    def test_qualified_types(self):
        declaration = body("A.B.C value = A.B.C()\n")[0]
        self.assertEqual(declaration.type.parts, ["A", "B", "C"])

    def test_signature_markers_and_variadics(self):
        function = body("int f(int a, /, int b = 1, *, str c, **float rest):\n    return a\n")[0]
        kinds = [p.kind for p in function.signature.parameters]
        self.assertEqual(kinds, ["normal", ParameterKind.SLASH, "normal", ParameterKind.STAR, "normal", ParameterKind.KWARG])

    def test_async_and_decorated_functions(self):
        function = body("@cache\nasync int f(int a):\n    return a\n")[0]
        self.assertTrue(function.is_async)
        self.assertEqual(len(function.decorators), 1)

    def test_elif_and_elunless_mix_in_one_chain(self):
        chain = body("if a:\n    pass\nelunless b:\n    pass\nelif c:\n    pass\nelse:\n    pass\n")[0]
        self.assertEqual([b.kind for b in chain.branches], ["if", "elunless", "elif"])
        self.assertEqual(len(chain.orelse), 1)

    def test_try_match_and_one_line_bodies(self):
        nodes = body(
            "try:\n    x()\nexcept (A, B) as e:\n    pass\nelse:\n    pass\nfinally:\n    pass\n"
            "match v:\n    case [1, *rest]:\n        pass\n    case _:\n        pass\n"
            "if ok: int y = 1; print(y)\n"
        )
        self.assertIsInstance(nodes[0], ast.Try)
        self.assertIsInstance(nodes[1], ast.Match)
        self.assertEqual(len(nodes[2].branches[0].body), 2)

    def test_match_as_a_name_is_still_a_name(self):
        self.assertIsInstance(body("dyn match = 1\nmatch = 2\n")[1], ast.Assign)

    def test_optional_chain_node(self):
        value = body("dyn r = a?.b[c](d)\n")[0].value
        self.assertIsInstance(value, OptionalChain)
        self.assertEqual([(l.kind, l.guarded) for l in value.links], [("attr", True), ("sub", False), ("call", False)])

    def test_plain_def_is_rejected_with_a_hint(self):
        with self.assertRaises(TypySyntaxError) as caught:
            body("def f():\n    pass\n")
        self.assertIn("typed signature", str(caught.exception))

    def test_orphan_clauses(self):
        for source in ("else:\n    pass\n", "elunless x:\n    pass\n", "except E:\n    pass\n"):
            with self.subTest(source=source), self.assertRaises(TypySyntaxError):
                body(source)

    def test_missing_block(self):
        with self.assertRaises(TypyIndentationError):
            body("until x:\nprint(1)\n")

    def test_declaration_without_value_gets_a_hint(self):
        with self.assertRaises(TypySyntaxError) as caught:
            body("int x\n")
        self.assertIn("needs a value", str(caught.exception))

    def test_bad_signatures(self):
        for source in ("int f(x):\n    pass\n", "int f(int a, int a):\n    pass\n",
                       "int f(int a = 1, int b):\n    pass\n", "int f(void a):\n    pass\n"):
            with self.subTest(source=source), self.assertRaises(TypySyntaxError):
                body(source)

    def test_keyword_used_as_identifier(self):
        with self.assertRaises(TypySyntaxError) as caught:
            body("until = 5\n")
        self.assertIn("reserved", str(caught.exception))
