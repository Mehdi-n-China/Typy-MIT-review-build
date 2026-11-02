"""Optional chaining (spec §24)."""

import unittest

from ._support import compile_errors, run_typy

_CLASSES = "class Obj:\n    None __init__(dyn self, **dyn fields):\n        self.__dict__.update(fields)\n\n"


class OptionalChainingTests(unittest.TestCase):
    def test_none_short_circuits(self):
        self.assertIsNone(run_typy("dyn user = None\ndyn r = user?.address?.city\n")["r"])

    def test_full_chain(self):
        ns = run_typy(_CLASSES + "dyn user = Obj(address=Obj(city='Montreal'))\ndyn r = user?.address?.city\n")
        self.assertEqual(ns["r"], "Montreal")

    def test_whole_rest_of_chain_is_skipped(self):
        self.assertIsNone(run_typy("dyn user = None\ndyn r = user?.address.state?.city\n")["r"])

    def test_call_arguments_are_not_evaluated_after_a_none(self):
        ns = run_typy("dyn calls = []\ndyn user = None\ndyn r = user?.method(calls.append(1))\n")
        self.assertEqual(ns["calls"], [])

    def test_unguarded_links_still_raise(self):
        with self.assertRaises(AttributeError):
            run_typy(_CLASSES + "dyn user = Obj(address=None)\ndyn r = user?.address.city\n")

    def test_subscript_and_method(self):
        ns = run_typy("dyn d = {'a': [10, 20]}\ndyn r = d?['a']?[1]\ndyn s = 'x'?.upper()\n")
        self.assertEqual((ns["r"], ns["s"]), (20, "X"))

    def test_nested_chains_in_arguments_and_keys(self):
        ns = run_typy("dyn a = None\ndyn r = [a?.b, {'k': a?['x']}]\n")
        self.assertEqual(ns["r"], [None, {"k": None}])

    def test_chains_in_conditions_and_loops(self):
        ns = run_typy("dyn a = None\nint hits = 0\nunless a?.b:\n    hits += 1\nfor x in a?.items or []:\n    hits += 100\n")
        self.assertEqual(ns["hits"], 1)

    def test_invalid_uses(self):
        for source in ("dyn r = a?\n", "dyn r = a?.b?\n", "dyn r = a ?(1)\n", "a?.b = 1\n", "del a?.b\n"):
            with self.subTest(source=source):
                self.assertTrue(compile_errors(source))
