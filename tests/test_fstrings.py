"""Generated f-strings run on every supported Python, with the same result."""

import unittest

from ._fstring_scan import pre_312_incompatible_fstrings
from ._support import PACKAGE_DIR, compile_ok, run_typy

# Each value is an f-string expression written the 3.12 way (quote reuse,
# backslashes in fields); Typy must print it so 3.10 can read it too.
_CASES = {
    "nested_quotes": "f'{data['name']}!'",
    "both_quotes": "f'{data['name'] + \"x\"}'",
    "format_spec": "f'{data['n']:>{width}}|'",
    "conversion": "f'{data['name']!r:^12}'",
    "debug": "f'{width=}'",
    "nested_fstring": "f'{f'{width}'}'",
    "backslash": "f'{'\\n'.join(['a', 'b'])}'",
    "braces": "f'{{literal}} { {1: 2}[1] }'",
    "walrus": "f'{(w := width)}'",
}


class FStringTests(unittest.TestCase):
    def test_same_value_as_python(self):
        data, width = {"name": "typy", "n": 7}, 6
        source = "dyn data = {'name': 'typy', 'n': 7}\nint width = 6\n" + "".join(
            f"dyn {name} = {expression}\n" for name, expression in _CASES.items()
        )
        namespace = run_typy(source)
        for name, expression in _CASES.items():
            with self.subTest(case=name):
                self.assertEqual(namespace[name], eval(expression, {"data": data, "width": width}))

    def test_output_is_readable_by_older_pythons(self):
        source = "dyn data = {}\nint width = 1\n" + "".join(f"dyn {n} = {e}\n" for n, e in _CASES.items())
        self.assertEqual(pre_312_incompatible_fstrings(compile_ok(source).python_code), [])

    def test_the_shipped_compiler_is_readable_by_older_pythons(self):
        for path in PACKAGE_DIR.rglob("*.py"):
            if {"tests", "example_project", "source"} & set(path.relative_to(PACKAGE_DIR).parts):
                continue
            with self.subTest(module=path.relative_to(PACKAGE_DIR).as_posix()):
                self.assertEqual(pre_312_incompatible_fstrings(path.read_text(encoding="utf-8")), [])
